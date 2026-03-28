import sys
import logging

class IdaCompatLayer:
    def __init__(self):
        self.version = "unknown"
        self.is_headless = False
        self._detect_environment()

    def _detect_environment(self):
        try:
            import ida_pro
            # IDA 9.x removed ida_struct, check if it exists
            if hasattr(sys.modules, "ida_struct") and "ida_struct" in sys.modules:
                self.version = "8.x"
            else:
                self.version = "9.x"
        except ImportError:
            # We are outside IDA
            self.version = "external"
        
        logging.info(f"[IDA Compat] Detected IDA version environment: {self.version}")

    def init_idalib_if_headless(self, binary_path: str):
        """Only works on IDA 9.x+ with idalib installed"""
        if self.version != "external":
            return False
            
        try:
            import idalib
            idalib.enable_console_messages(True)
            if idalib.open_database(binary_path, True):
                self.is_headless = True
                self.version = "9.x-headless"
                logging.info(f"Successfully loaded {binary_path} via idalib")
                return True
            return False
        except ImportError:
            logging.error("idalib not found. Ensure IDA 9.0+ idalib is installed in python env")
            return False

compat = IdaCompatLayer()
