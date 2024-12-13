import hashlib
import numpy as np
from PIL import Image
import sys
import logging


class AdvancedImageHashSpoofer:
    def __init__(self, hash_algorithm=hashlib.sha512):
        """
        Advanced Image Hash Spoofer with multiple spoofing strategies

        Args:
            hash_algorithm (hashlib._hashlib.HASH, optional): Hash algorithm to use. Defaults to SHA-512.
        """
        self.hash_algorithm = hash_algorithm
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _generate_targeted_noise(self, image_array, target_prefix):
        """
        Generate more targeted noise for hash manipulation

        Args:
            image_array (np.ndarray): Original image array
            target_prefix (str): Target hash prefix

        Returns:
            np.ndarray: Noise array
        """
        # Convert target prefix to target bytes
        target_bytes = bytes.fromhex(target_prefix.replace('0x', ''))

        # Create noise with structured approach
        noise = np.zeros_like(image_array, dtype=np.float32)

        # Multiple noise generation strategies
        strategies = [
            # Gaussian noise with controlled magnitude
            lambda: np.random.normal(0, 0.5, image_array.shape),

            # Structured perturbation in specific channels
            lambda: np.random.uniform(-1, 1,
                                      image_array.shape) * (image_array / 255),

            # Localized noise in specific image regions
            lambda: np.random.normal(
                0, 1, image_array.shape) * (np.random.random(image_array.shape) < 0.1)
        ]

        return np.clip(
            image_array + strategies[np.random.randint(0, len(strategies))](),
            0, 255
        ).astype(np.uint8)

    def spoof_image(self, input_path, output_path, target_prefix, max_attempts=50000):
        """
        Advanced image hash spoofing with multiple strategies

        Args:
            input_path (str): Input image path
            output_path (str): Output image path
            target_prefix (str): Target hash prefix
            max_attempts (int): Maximum spoofing attempts

        Returns:
            bool: Spoofing success
        """
        # Open and convert image
        img = Image.open(input_path)
        img_array = np.array(img)

        # Detailed logging
        self.logger.info(f"Attempting to spoof hash prefix: {target_prefix}")
        self.logger.info(f"Image dimensions: {img_array.shape}")
        self.logger.info(f"Image dtype: {img_array.dtype}")

        # Multiple spoofing attempts
        for attempt in range(max_attempts):
            # Generate perturbed image
            perturbed_array = self._generate_targeted_noise(
                img_array, target_prefix)

            # Compute hash
            current_hash = hashlib.sha512(
                perturbed_array.tobytes()).hexdigest()

            # Check hash prefix
            if current_hash.startswith(target_prefix.replace('0x', '')):
                self.logger.info(f"Success on attempt {attempt + 1}")
                self.logger.info(f"Matched hash: {current_hash}")

                # Save spoofed image
                spoofed_img = Image.fromarray(perturbed_array)
                spoofed_img.save(output_path)

                return True

            # Periodic logging for long-running attempts
            if attempt % 1000 == 0:
                self.logger.info(
                    f"Attempt {attempt}: Current hash does not match")

        self.logger.error("Could not spoof image hash within attempts")
        return False


def main():
    if len(sys.argv) != 4:
        print("Usage: python image_hash_spoofer.py <target_prefix> <input_image> <output_image>")
        sys.exit(1)

    target_prefix = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    spoofer = AdvancedImageHashSpoofer()
    success = spoofer.spoof_image(input_path, output_path, target_prefix)

    if success:
        print(f"Image hash spoofed successfully. New hash starts with {
              target_prefix}")
    else:
        print("Hash spoofing failed.")


if __name__ == "__main__":
    main()
