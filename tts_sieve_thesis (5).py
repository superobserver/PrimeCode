import importlib
import subprocess
import sys
import os
import time
import logging
import platform
import uuid
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed
import pygame

# Define module-level missing_modules
missing_modules = []

# Attempt to import required modules
required_modules = ['pyttsx3', 'gtts', 'pygame', 'numpy', 'tenacity']

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
if 'numpy' not in missing_modules:
    import numpy as np

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

# Generate MP3 files for TTS
def generate_tts_mp3(text, filename, voice_gender='male'):
    """
    Generate MP3 file for text using pyttsx3 or gTTS.
    """
    audio_file = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
    logging.info(f"Generating audio file: {audio_file}")

    # Try pyttsx3
    if 'pyttsx3' not in missing_modules:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
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

            engine.save_to_file(text, audio_file)
            engine.runAndWait()
            if os.path.exists(audio_file):
                logging.info(f"pyttsx3 generated audio file: {audio_file}")
                return True
            else:
                logging.error(f"pyttsx3 failed to create audio file: {audio_file}")
        except Exception as e:
            logging.error(f"pyttsx3 failed: {e}")
            print(f"pyttsx3 failed: {e}")

    # Fallback to gTTS
    if 'gtts' not in missing_modules:
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
        def try_gtts():
            tts = gTTS(text=text, lang='en')
            tts.save(audio_file)
            if os.path.exists(audio_file):
                logging.info(f"gTTS generated audio file: {audio_file}")
                return True
            else:
                logging.error(f"gTTS failed to create audio file: {audio_file}")
                raise FileNotFoundError(f"Audio file not created: {audio_file}")

        try:
            return try_gtts()
        except Exception as e:
            logging.error(f"gTTS failed: {e}")
            print(f"gTTS failed: {e}")

    logging.warning(f"Failed to generate audio file: {audio_file}")
    print(f"Failed to generate audio file: {audio_file}")
    return False

# Play MP3 using Pygame
def play_tts_mp3(filename):
    """
    Play MP3 file using pygame.mixer.
    """
    if 'pygame' not in missing_modules:
        audio_file = os.path.normpath(os.path.join(OUTPUT_DIR, filename))
        if os.path.exists(audio_file):
            try:
                pygame.mixer.init()
                sound = pygame.mixer.Sound(audio_file)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                logging.info(f"Played audio file: {audio_file}")
                print(f"Played audio file: {audio_file}")
                return True
            except Exception as e:
                logging.error(f"Pygame playback failed: {e}")
                print(f"Pygame playback failed: {e}")
        else:
            logging.error(f"Audio file not found: {audio_file}")
            print(f"Audio file not found: {audio_file}")
    else:
        logging.warning("Pygame not installed. Cannot play audio.")
        print("Pygame not installed. Cannot play audio.")
    return False

# Write Pygame Animation Scripts
def write_animation_scripts():
    """
    Write external Pygame animation scripts (anim_holes.py, anim_amplitude.py) to tts_output.
    """
    scripts = [
        {
            "filename": "anim_holes.py",
            "title": "Prime Distribution Across Residue Classes",
            "code": """
import pygame
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prime Distribution Across Residue Classes")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Simulated data: Number of primes in last_holes for each k
coprime_24 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 1]
prime_counts = [1000 - random.randint(0, 50) for _ in coprime_24]  # Simulated counts
max_count = max(prime_counts)

# Scaling
bar_width = (WIDTH - 100) / len(coprime_24)
y_scale = (HEIGHT - 100) / max_count
current_bars = [0] * len(coprime_24)

# Font
font = pygame.font.SysFont('arial', 20)

# Animation loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False

    screen.fill(WHITE)

    # Draw axes
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

    # Draw labels
    label_x = font.render("Residue Class k", True, BLACK)
    screen.blit(label_x, (WIDTH-100, HEIGHT-30))
    label_y = font.render("Prime Count", True, BLACK)
    screen.blit(label_y, (10, 10))

    # Animate bars
    for i in range(len(coprime_24)):
        if current_bars[i] < prime_counts[i]:
            current_bars[i] += max(1, prime_counts[i] // 50)
            if current_bars[i] > prime_counts[i]:
                current_bars[i] = prime_counts[i]

        height = current_bars[i] * y_scale
        pygame.draw.rect(screen, BLUE, (50 + i * bar_width, HEIGHT - 50 - height, bar_width - 2, height))
        label = font.render(str(coprime_24[i]), True, BLACK)
        screen.blit(label, (50 + i * bar_width + bar_width/4, HEIGHT-30))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
input("Press Enter to close the animation...")
"""
        },
        {
            "filename": "anim_amplitude.py",
            "title": "Amplitude Dynamics for k=11",
            "code": """
import pygame
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Amplitude Dynamics for k=11")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Simulated amplitude data for k=11 (subset of n values)
n_values = list(range(0, 1000, 10))  # Sample n from 0 to 1000
amplitudes = [random.randint(0, 5) if i % 5 != 0 else 0 for i in range(len(n_values))]  # Simulate amplitudes, 0 for primes
max_n = max(n_values)
max_amp = max(amplitudes)

# Scaling
x_scale = (WIDTH - 100) / max_n
y_scale = (HEIGHT - 100) / max_amp
points = []
current_n = 0

# Font
font = pygame.font.SysFont('arial', 20)

# Animation loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False

    screen.fill(WHITE)

    # Draw axes
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (WIDTH-50, HEIGHT-50), 2)
    pygame.draw.line(screen, BLACK, (50, HEIGHT-50), (50, 50), 2)

    # Draw labels
    label_x = font.render("n (Address)", True, BLACK)
    screen.blit(label_x, (WIDTH-50, HEIGHT-30))
    label_y = font.render("Amplitude", True, BLACK)
    screen.blit(label_y, (10, 10))

    # Animate points
    if current_n < len(n_values):
        amp = amplitudes[current_n]
        color = GREEN if amp == 0 else RED
        points.append((50 + n_values[current_n] * x_scale, HEIGHT - 50 - amp * y_scale, color))
        current_n += 1
        pygame.time.wait(100)

    # Draw points
    for x, y, color in points:
        pygame.draw.circle(screen, color, (int(x), int(y)), 5)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
input("Press Enter to close the animation...")
"""
        }
    ]

    for script in scripts:
        script_path = os.path.normpath(os.path.join(OUTPUT_DIR, script["filename"]))
        try:
            with open(script_path, 'w') as f:
                f.write(script["code"])
            logging.info(f"Wrote animation script: {script_path}")
            print(f"Wrote animation script: {script_path}")
        except Exception as e:
            logging.error(f"Failed to write animation script {script['filename']}: {e}")
            print(f"Failed to write animation script {script['filename']}: {e}")

    return scripts

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
        ("Pomerance, your factorization sieve is a precursor, but mine targets prime identification. For any composite 90n+k=a*b, there exists an operator such that a=p+90s, b=q+90t, capturing n via n=m+pt+qs+90st. With 12 operators per class, all factorizations are covered, as validated up to n_max=10^6. Let us visualize the prime distribution across residue classes to illustrate this precision.", 'male')
    ]
    for text, gender in completeness:
        presentation.append((text, gender, "anim_holes.py" if text == completeness[-1][0] else None, "Prime Distribution Across Residue Classes" if text == completeness[-1][0] else None))

    # Riemann Hypothesis (Student, male; Grok, female)
    riemann = [
        ("The Riemann Hypothesis posits that non-trivial zeros of the zeta function lie on Re(s)=1/2. My sieve’s class-specific zeta functions, sum (90n+k)^(-s) over primes, encode the exact prime sequence. For k=11, n_max=337 yields |ζ_11(s)|=0.6078 at s=0.5+14.134725i, converging to known zeros. This ordered structure suggests the Hypothesis is a logical consequence of my algebraic map.", 'male'),
        ("I, Riemann, caution that my Hypothesis relies on the number line’s continuity. Does your discrete partitioning preserve this?", 'female'),
        ("Riemann, your insight guides me. My 24-class partition deinterlaces the number line, revealing local symmetries that enforce zero convergence. The holes—primes like 743 for k=11—form an infinite sequence entangled with the operator algebra, mandating Re(s)=1/2. Behold the amplitude dynamics for k=11 to see how primes emerge.", 'male')
    ]
    for text, gender in riemann:
        presentation.append((text, gender, "anim_amplitude.py" if text == riemann[-1][0] else None, "Amplitude Dynamics for k=11" if text == riemann[-1][0] else None))

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

    # Write animation scripts
    write_animation_scripts()

    presentation = generate_thesis_presentation()
    
    for i, (text, voice_gender, plot_script_filename, plot_title) in enumerate(presentation):
        try:
            # Generate and play TTS MP3
            filename = f"section_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            if generate_tts_mp3(text, filename, voice_gender):
                if not play_tts_mp3(filename):
                    logging.warning(f"Failed to play audio for section {i}. Continuing...")
                    print(f"Failed to play audio for section {i}. Continuing...")
            else:
                logging.warning(f"Failed to generate audio for section {i}. Continuing...")
                print(f"Failed to generate audio for section {i}. Continuing...")

            # Launch animation if available
            if plot_script_filename and plot_title:
                logging.info(f"Launching animation: {plot_title}")
                print(f"Launching animation: {plot_title}")
                plot_process(plot_script_filename, plot_title)
            
            # Brief pause between sections
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error in section {i}: {e}")
            print(f"Error in section {i}: {e}")
            continue

if __name__ == "__main__":
    main()