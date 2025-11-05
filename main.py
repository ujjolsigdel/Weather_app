import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather ☁", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(500, 600)

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#74ABE2"))
        gradient.setColorAt(1.0, QColor("#5563DE"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(30, 30, 30, 30)
        vbox.setSpacing(20)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.get_weather_button)

        vbox.addWidget(self.city_label, alignment=Qt.AlignCenter)
        vbox.addLayout(input_layout)
        vbox.addSpacing(30)
        vbox.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.emoji_label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.description_label, alignment=Qt.AlignCenter)
        vbox.addStretch()

        self.setLayout(vbox)
        self.city_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.city_label.setStyleSheet("color: white;")

        self.city_input.setFont(QFont("Segoe UI", 18))
        self.city_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border-radius: 20px;
                padding: 10px 20px;
                border: 2px solid #ccc;
            }
            QLineEdit:focus {
                border: 2px solid #74ABE2;
            }
        """)

        self.get_weather_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.get_weather_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB74D;
                border-radius: 20px;
                padding: 10px 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: #FFA726;
            }
            QPushButton:pressed {
                background-color: #F57C00;
            }
        """)

        self.temperature_label.setFont(QFont("Segoe UI", 60, QFont.Bold))
        self.temperature_label.setStyleSheet("color: white;")
        self.emoji_label.setFont(QFont("Segoe UI Emoji", 100))
        self.description_label.setFont(QFont("Segoe UI", 28, QFont.Medium))
        self.description_label.setStyleSheet("color: #E3F2FD; text-transform: capitalize;")
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)  # 👈 Enter triggers weather search

    def get_weather(self):
        api_key = "12469a769d35b344913147a7c81084a0"
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.RequestException:
            self.display_error("⚠ Network Error\nPlease check your connection.")
        except Exception as e:
            self.display_error(f"Error: {str(e)}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("color: #FFCDD2; font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("color: white; font-size: 60px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return "🌈"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
