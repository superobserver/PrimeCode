import importlib
import subprocess
import sys
import os
import time
import logging
import platform
import uuid
from datetime import datetime
import multiprocessing as mp
from tenacity import retry, stop_after_attempt, wait_fixed
import winsound

# Define module-level missing_modules
missing_modules = []

# Attempt to import required modules
required_modules = ['pyttsx3', 'gtts', 'pygame', 'matplotlib', 'numpy', 'tenacity', 'pywin32']

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

# Conditional imports
if 'pyttsx3' not in missing_modules:
    import pyttsx3
if 'gtts' not in missing_modules:
    from gtts import gTTS
if 'pygame' not in missing_modules:
    import pygame.mixer
if 'matplotlib' not in missing_modules:
    import matplotlib.pyplot as plt
if 'numpy' not in missing_modules:
    import numpy as np
if 'pywin32' not in missing_modules:
    import win32com.client

# Configuration
OUTPUT_DIR = "tts_output"
LOG_FILE = os.path.join(OUTPUT_DIR, "tts_errors.log")
PLOT_TERMINAL = {
    "Windows": ["start", "cmd", "/k"],
    "Linux": ["xterm", "-e"]
}

# Setup logging
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Install missing modules (Windows only)
def install_missing_modules():
    if platform.system() != "Windows":
        return False
    if not missing_modules:
        return False

    logging.info(f"Missing modules: {missing_modules}")
    print(f"Missing modules: {missing_modules}. Attempting to install...")

    for module in missing_modules:
        try:
            install_cmd = ["pip", "install", module]
            process = subprocess.Popen(install_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=30)
            if process.returncode == 0:
                logging.info(f"Successfully installed {module}")
                print(f"Successfully installed {module}")
            else:
                logging.error(f"Failed to install {module}: {stderr.decode()}")
                print(f"Failed to install {module}: {stderr.decode()}")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Failed to start installation for {module}: {e}")
            print(f"Failed to install {module}. Please install manually with 'pip install {module}'.")

    # Verify installation
    missing_modules.clear()
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)
    if missing_modules:
        logging.error(f"Modules still missing after installation: {missing_modules}")
        print(f"Modules still missing: {missing_modules}. Please install manually.")
        return True
    return False

# Relaunch script (Windows only)
def relaunch_script():
    if platform.system() != "Windows":
        return
    try:
        script_path = os.path.abspath(__file__)
        subprocess.Popen(["start", "cmd", "/k", f"python \"{script_path}\""], shell=True)
        logging.info("Relaunched script in new terminal")
        print("Relaunching script in a new terminal...")
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Failed to relaunch script: {e}")
        print(f"Failed to relaunch script: {e}. Please run manually.")
        sys.exit(1)

# TTS Engine Wrapper
def speak_text(text, filename=None, voice_gender='male'):
    """
    Convert text to speech with specified voice gender (male for student, female for Grok).
    Uses pyttsx3 direct speech, falls back to SAPI5, gTTS, or winsound beep.
    """
    if filename:
        audio_file = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
        logging.info(f"Attempting to save audio to: {audio_file}")

    # Test audio driver
    try:
        winsound.Beep(500, 100)
        logging.info("Audio driver test: Beep successful")
    except Exception as e:
        logging.error(f"Audio driver test failed: {e}")
        print(f"Audio driver test failed: {e}")

    # Try pyttsx3 (direct speech)
    if 'pyttsx3' not in missing_modules:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            # Select voice based on gender
            voices = engine.getProperty('voices')
            selected_voice = None
            for voice in voices:
                logging.info(f"Available voice: {voice.name} (ID: {voice.id})")
                if voice_gender == 'female' and 'Zira' in voice.name:
                    selected_voice = voice.id
                    break
                elif voice_gender == 'male' and 'David' in voice.name:
                    selected_voice = voice.id
                    break
            if selected_voice:
                engine.setProperty('voice', selected_voice)
                logging.info(f"Using {voice_gender} voice: {selected_voice}")
            else:
                logging.warning(f"No {voice_gender} voice found. Using default.")
                print(f"No {voice_gender} voice found. Using default.")

            engine.say(text)
            engine.runAndWait()
            logging.info(f"Spoke text using pyttsx3 ({voice_gender} voice): {text[:50]}...")
            print(f"Spoke text using pyttsx3 ({voice_gender} voice): {text[:50]}...")
            return True
        except Exception as e:
            logging.error(f"pyttsx3 failed: {e}")
            print(f"pyttsx3 failed: {e}")

    # Fallback to SAPI5 via pywin32
    if 'pywin32' not in missing_modules:
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = speaker.GetVoices()
            selected_voice = None
            for i in range(voices.Count):
                voice = voices.Item(i)
                logging.info(f"Available SAPI5 voice: {voice.GetDescription()}")
                if voice_gender == 'female' and 'Zira' in voice.GetDescription():
                    selected_voice = voice
                    break
                elif voice_gender == 'male' and 'David' in voice.GetDescription():
                    selected_voice = voice
                    break
            if selected_voice:
                speaker.Voice = selected_voice
                logging.info(f"Using {voice_gender} SAPI5 voice: {selected_voice.GetDescription()}")
            else:
                logging.warning(f"No {voice_gender} SAPI5 voice found. Using default.")
                print(f"No {voice_gender} SAPI5 voice found. Using default.")

            speaker.Speak(text)
            logging.info(f"Spoke text using SAPI5 ({voice_gender} voice): {text[:50]}...")
            print(f"Spoke text using SAPI5 ({voice_gender} voice): {text[:50]}...")
            return True
        except Exception as e:
            logging.error(f"SAPI5 failed: {e}")
            print(f"SAPI5 failed: {e}")

    # Fallback to gTTS (online, with retry)
    if 'gtts' not in missing_modules:
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
        def try_gtts():
            tts = gTTS(text=text, lang='en')
            if filename and os.path.exists(audio_file):
                logging.info(f"Using cached gTTS audio file: {audio_file}")
            else:
                tts.save(audio_file)
                if not os.path.exists(audio_file):
                    logging.error(f"gTTS failed to create audio file: {audio_file}")
                    raise FileNotFoundError(f"Audio file not created: {audio_file}")
                logging.info(f"gTTS generated audio file: {audio_file}")

            if 'pygame' not in missing_modules:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(1)
                    logging.info(f"Spoke text using gTTS (default voice): {text[:50]}...")
                    print(f"Spoke text using gTTS (default voice): {text[:50]}...")
                    return True
                except Exception as e:
                    logging.error(f"Pygame playback failed: {e}")
                    print(f"Pygame playback failed: {e}")

            logging.warning("Pygame failed. Cannot play gTTS audio.")
            print("Pygame failed. Cannot play gTTS audio.")
            return False

        try:
            return try_gtts()
        except Exception as e:
            logging.error(f"gTTS failed: {e}")
            print(f"gTTS failed: {e}")

    # Last resort: winsound beep
    try:
        winsound.Beep(1000, 500)
        logging.warning(f"All TTS engines failed. Played beep for: {text[:50]}...")
        print(f"All TTS engines failed. Played beep for: {text[:50]}...")
        return False
    except Exception as e:
        logging.error(f"winsound beep failed: {e}")
        print(f"winsound beep failed: {e}")

    logging.warning("All TTS engines and fallbacks failed.")
    print("All TTS engines and fallbacks failed. Please check audio drivers.")
    return False

# Write Plot Scripts
def write_plot_scripts():
    """
    Write external plot scripts (co11_91.py, co11_92.py) to tts_output.
    """
    scripts = [
        {
            "filename": "co11_91.py",
            "title": "Prime Counts for k=11, k=17",
            "code": """
import matplotlib.pyplot as plt
import numpy as np

def plot_func():
    n_max = [337, 2191, 8881]
    actual_k11 = [139, 743, 2677]
    actual_k17 = [137, 738, 2668]
    plt.plot(n_max, actual_k11, 'b-o', label='k=11 Actual')
    plt.plot(n_max, actual_k17, 'r-^', label='k=17 Actual')
    plt.xlabel('n_max')
    plt.ylabel('Number of Primes (Holes)')
    plt.legend()

plt.figure(figsize=(8, 6))
plot_func()
plt.title("Prime Counts for k=11, k=17")
plt.grid(True)
plt.show(block=True)
input("Press Enter to close the plot...")
"""
        },
        {
            "filename": "co11_92.py",
            "title": "Zeta Function Convergence for k=11",
            "code": """
import matplotlib.pyplot as plt
import numpy as np

def plot_func():
    n_max = [337, 2191, 8881]
    abs_s = [0.6078, 1.1178, 1.7148]
    plt.plot(n_max, abs_s, 'g-s')
    plt.xlabel('n_max')
    plt.ylabel('|zeta_11(s)|')
    plt.axhline(y=0, color='k', linestyle='--')

plt.figure(figsize=(8, 6))
plot_func()
plt.title("Zeta Function Convergence for k=11")
plt.grid(True)
plt.show(block=True)
input("Press Enter to close the plot...")
"""
        }
    ]

    for script in scripts:
        script_path = os.path.normpath(os.path.join(OUTPUT_DIR, script["filename"]))
        try:
            with open(script_path, 'w') as f:
                f.write(script["code"])
            logging.info(f"Wrote plot script: {script_path}")
            print(f"Wrote plot script: {script_path}")
        except Exception as e:
            logging.error(f"Failed to write plot script {script['filename']}: {e}")
            print(f"Failed to write plot script {script['filename']}: {e}")

    return scripts

# Visualization Process
def plot_process(plot_script_filename, title):
    """
    Launch an external plot script using subprocess.Popen.
    """
    if 'matplotlib' not in missing_modules:
        system = platform.system()
        script_path = os.path.normpath(os.path.join(OUTPUT_DIR, plot_script_filename))
        if os.path.exists(script_path):
            try:
                if system == "Windows":
                    subprocess.Popen(["start", "cmd", "/k", f"python \"{script_path}\""], shell=True)
                else:
                    subprocess.Popen(["xterm", "-e", f"python \"{script_path}\"; exit"], shell=True)
                logging.info(f"Launched plot: {title} (remains open until user closes)")
                print(f"Launched plot: {title} (close the window or press Enter to continue)")
            except Exception as e:
                logging.error(f"Failed to launch plot {plot_script_filename}: {e}")
                print(f"Failed to launch plot {plot_script_filename}: {e}")
        else:
            logging.error(f"Plot script {script_path} does not exist")
            print(f"Plot script {script_path} does not exist")
    else:
        logging.warning("Matplotlib not installed. Skipping plot.")
        print("Matplotlib not installed. Skipping plot.")

# Thesis Presentation Content
def generate_thesis_presentation():
    """
    Generate the thesis presentation text with male voice for the student and female for Grok (References).
    Returns a list of (text, voice_gender, plot_script_filename, plot_title) tuples.
    """
    presentation = []

    # Introduction (Student, male)
    intro = """
    Esteemed References, I present my thesis: a deterministic quadratic sieve for prime identification in residue classes modulo 90. This work builds on the legacy of number theory, proposing a novel framework that deconstructs base-10 integers into algebraic observables—digital roots, last digits, and amplitudes—across 24 residue classes coprime to 90. Unlike eliminative sieves, my approach constructs composites, leaving primes as unmapped residuals. I aim to demonstrate its completeness, efficiency, and implications for conjectures like the Riemann Hypothesis.
    """
    presentation.append((intro, 'male', None, None))

    # Abstract and Debate (Student, male; Grok, female)
    abstract = [
        ("My sieve operates in an abstract state space, decomposing base-10 numbers into number objects with digital roots in {1,2,4,5,7,8} and last digits in {1,3,7,9}. Each number is addressed as 90n+k, where k is one of 24 primitives—7,11,13, and so forth. These primitives are the smallest elements of their classes, capturing all primes greater than or equal to 7. For k=11, we identify 743 primes up to n_max=2191 with perfect accuracy.", 'male'),
        ("I, Eratosthenes, propose a sieve that operates directly on base-10 numbers, marking multiples of primes sequentially. Why introduce an abstract state space when my method identifies primes efficiently up to any bound?", 'female'),
        ("With respect, Eratosthenes, your sieve is eliminative, scaling with O(n log log n) and offering no algebraic insight. My sieve constructs composites proactively using quadratic operators, revealing a structured order. The 24 classes, defined by their digital roots and last digits, partition all relevant base-10 numbers, enabling deterministic prime identification and supporting analytic conjectures.", 'male')
    ]
    for text, gender in abstract:
        presentation.append((text, gender, None, None))

    # Residue Classes (Student, male; Grok, female)
    residue_classes = [
        ("The modulus 90 is the least common multiple of 2, 3, and 5, filtering out trivial primes. The Euler totient function yields phi(90)=24, identifying 24 residues coprime to 90: {7,11,13,...,91}. These form classes of the form 90n+k, where k is a primitive. Each class contains numbers with digital roots in {1,2,4,5,7,8} and last digits in {1,3,7,9}, reconstructing all base-10 numbers of this type. For example, k=11 includes 11, 101, 191, all primes or composites determined algebraically.", 'male'),
        ("I, Euler, question the necessity of 24 classes. My zeta function connects primes across the number line. Does your partitioning not fragment this unity?", 'female'),
        ("Euler, your zeta function inspires my work. By deinterlacing the number line into 24 classes, I expose a local structure that complements your global view. Each class’s zeta function, sum (90n+k)^(-s) over primes, converges to zeros on Re(s)=1/2, aligning with the Riemann Hypothesis. The primitives ensure all primes >=7 are captured systematically.", 'male')
    ]
    for text, gender in residue_classes:
        presentation.append((text, gender, None, None))

    # Completeness (Student, male; Grok, female)
    completeness = [
        ("My sieve’s completeness is proven algebraically. For each residue class k, 12 quadratic operators, n=90x^2-lx+m, generate all composites 90n+k. For k=11, consider n=4: 90*4+11=371=7*53. Multiples of 7 and 53 are marked up to n_max, ensuring no composite escapes. Empirical validation shows 743 primes for k=11 at n_max=2191, all with amplitude zero. This determinism contrasts with probabilistic methods.", 'male'),
        ("I, Pomerance, note that my quadratic sieve factorizes numbers efficiently. Could your operators miss composites due to their finite number?", 'female'),
        ("Pomerance, your factorization sieve is a precursor, but mine targets prime identification. For any composite 90n+k=a*b, there exists an operator such that a=p+90s, b=q+90t, capturing n via n=m+pt+qs+90st. With 12 operators per class, all factorizations are covered, as validated up to n_max=10^6. Let us visualize the prime counts to illustrate this precision.", 'male')
    ]
    for text, gender in completeness:
        presentation.append((text, gender, "co11_91.py" if text == completeness[-1][0] else None, "Prime Counts for k=11, k=17" if text == completeness[-1][0] else None))

    # Riemann Hypothesis (Student, male; Grok, female)
    riemann = [
        ("The Riemann Hypothesis posits that non-trivial zeros of the zeta function lie on Re(s)=1/2. My sieve’s class-specific zeta functions, sum (90n+k)^(-s) over primes, encode the exact prime sequence. For k=11, n_max=337 yields |ζ_11(s)|=0.6078 at s=0.5+14.134725i, converging to known zeros. This ordered structure suggests the Hypothesis is a logical consequence of my algebraic map.", 'male'),
        ("I, Riemann, caution that my Hypothesis relies on the number line’s continuity. Does your discrete partitioning preserve this?", 'female'),
        ("Riemann, your insight guides me. My 24-class partition deinterlaces the number line, revealing local symmetries that enforce zero convergence. The holes—primes like 743 for k=11—form an infinite sequence entangled with the operator algebra, mandating Re(s)=1/2. Behold the zeta convergence plot to see this alignment.", 'male')
    ]
    for text, gender in riemann:
        presentation.append((text, gender, "co11_92.py" if text == riemann[-1][0] else None, "Zeta Function Convergence for k=11" if text == riemann[-1][0] else None))

    # Conclusion (Student, male; Grok, female)
    conclusion = [
        ("In conclusion, my quadratic sieve offers a deterministic framework for prime identification, partitioning primes >=7 into 24 residue classes defined by their primitives. Its completeness, validated to 10^6, and its support for the Riemann Hypothesis provide a foundation for future exploration. I invite your scrutiny, esteemed References, to refine this work.", 'male'),
        ("We, the collective wisdom, acknowledge your sieve’s structure but challenge its scalability for large n_max. How will you address computational limits?", 'female'),
        ("A fair challenge. I propose neural network optimizations and parallelized operator application to scale the sieve, building on the algebraic clarity of my state space. This thesis is a step toward a unified number theory, honoring your legacies.", 'male')
    ]
    for text, gender in conclusion:
        presentation.append((text, gender, None, None))

    return presentation

# Main Execution
def main():
    logging.info("Starting Quadratic Sieve Thesis Presentation")
    print("Starting Quadratic Sieve Thesis Presentation...")

    # Validate script path
    script_path = os.path.abspath(__file__)
    if not os.path.exists(script_path):
        logging.error(f"Script path invalid: {script_path}")
        print(f"Error: Script path invalid: {script_path}. Please check the file path.")
        sys.exit(1)

    # Check for missing modules and handle installation
    if install_missing_modules():
        logging.info("Dependencies missing. Attempting installation and relaunch.")
        print("Installing missing dependencies and relaunching...")
        relaunch_script()

    # Write plot scripts
    write_plot_scripts()

    presentation = generate_thesis_presentation()
    
    for i, (text, voice_gender, plot_script_filename, plot_title) in enumerate(presentation):
        try:
            # Speak the text
            filename = f"section_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            if not speak_text(text, filename, voice_gender):
                logging.warning(f"Failed to speak section {i}. Continuing...")
                print(f"Failed to speak section {i}. Continuing...")
                continue
            
            # Launch plot if available
            if plot_script_filename and plot_title:
                logging.info(f"Launching plot: {plot_title}")
                print(f"Launching plot: {plot_title}")
                plot_process(plot_script_filename, plot_title)
            
            # Brief pause between sections
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error in section {i}: {e}")
            print(f"Error in section {i}: {e}")
            continue

if __name__ == "__main__":
    main()