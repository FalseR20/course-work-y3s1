from PyQt6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main window
        self.setWindowTitle("Crypto-predictor")

        # Central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Currencies
        self.currencies_group = QtWidgets.QGroupBox()
        self.central_widget_layout.addWidget(self.currencies_group)
        self.currencies_layout = QtWidgets.QHBoxLayout(self.currencies_group)
        self.currency = QtWidgets.QComboBox()
        self.currencies_layout.addWidget(self.currency)
        self.base_currency = QtWidgets.QComboBox()
        self.currencies_layout.addWidget(self.base_currency)

        # Graph (stub)
        self.graph_widget = QtWidgets.QLabel()
        self.central_widget_layout.addWidget(self.graph_widget)
        self.graph_widget.setStyleSheet("*{ background-color: #222; }")

        # Control panel
        self.control_group = QtWidgets.QGroupBox()
        self.central_widget_layout.addWidget(self.control_group)
        self.control_group_layout = QtWidgets.QHBoxLayout(self.control_group)
        self.control_checkbox_run = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_run)
        self.control_checkbox_run.setText("Run")
        self.control_checkbox_learn = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_learn)
        self.control_checkbox_learn.setText("Learn")
        self.control_checkbox_predicate = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_predicate)
        self.control_checkbox_predicate.setText("Predicate")
