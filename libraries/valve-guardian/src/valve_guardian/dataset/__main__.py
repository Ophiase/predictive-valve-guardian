import logging

from valve_guardian.dataset import HydraulicArchive

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    HydraulicArchive().download()
