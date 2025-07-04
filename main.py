import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer
from app.gui import PDFQAApp


# Global variables for splash screen animation
splash_dot_count = 0
splash_timer = None
splash_screen_instance = None # To hold the reference to the splash screen



def update_splash_message():
    """Updates the splash screen message with animated dots."""
    global splash_dot_count, splash_screen_instance
    if splash_screen_instance:
        splash_dot_count = (splash_dot_count + 1) % 4 # Cycle through 0, 1, 2, 3 dots
        dots = "." * splash_dot_count
        splash_screen_instance.showMessage(f"Loading IntelliPDF{dots}",
                                           Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                                           Qt.GlobalColor.white)

def show_main_app():
    """Function to create and show the main application window."""
    global main_window, splash_timer
    if splash_timer:
        splash_timer.stop() # Stop the dot animation timer when main app loads
    main_window = PDFQAApp()
    main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Create the QSplashScreen instance
    splash_pixmap = QPixmap(600, 300) # Create a QPixmap (e.g., 600x300 pixels)
    splash_pixmap.fill(Qt.GlobalColor.black) # Fill it with black background
    
    # Removed 'global splash_screen_instance' here as it's already global
    splash_screen_instance = QSplashScreen(splash_pixmap)
    splash_screen_instance.setFont(QFont("Segoe UI", 18))
    
    # Initial message
    splash_screen_instance.showMessage("Loading IntelliPDF...",
                                      Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                                      Qt.GlobalColor.white)
    splash_screen_instance.show()

    # 2. Set up a QTimer for dot animation
    # Removed 'global splash_timer' here as it's already global
    splash_timer = QTimer()
    splash_timer.timeout.connect(update_splash_message)
    splash_timer.start(500) # Update dots every 500 milliseconds

    # 3. Set a timer to close the splash screen and show the main app
    # The splash screen will be visible for 3000 milliseconds (3 seconds)
    QTimer.singleShot(3000, splash_screen_instance.close) # Close the splash screen
    QTimer.singleShot(3000, show_main_app) # Show the main app after the delay

    # 4. Start the application event loop
    sys.exit(app.exec())