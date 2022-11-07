import logging
from parser import base_currencies, client, crypto_currencies

from PyQt6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log = lambda *args_, **kwargs_: logging.log(logging.DEBUG + 5, *args_, **kwargs_)

        # Main window
        self.setWindowTitle("Crypto-predictor")
        self.setMinimumSize(300, 180)
        self.resize(1000, 500)

        # Central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Currencies
        self.currencies_group = QtWidgets.QGroupBox()
        self.currencies_group.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currencies_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.currencies_layout = QtWidgets.QHBoxLayout(self.currencies_group)
        self.central_widget_layout.addWidget(self.currencies_group)

        # Crypto currency combobox
        self.crypto_currency = QtWidgets.QComboBox()
        self.crypto_currency.setMaxVisibleItems(30)
        self.currencies_layout.addWidget(self.crypto_currency)

        # Label between comboboxes '/'
        label = QtWidgets.QLabel(" / ")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.currencies_layout.addWidget(label)

        # Base currency combobox
        self.base_currency = QtWidgets.QComboBox()
        self.base_currency.setMaxVisibleItems(30)
        self.currencies_layout.addWidget(self.base_currency)

        # Graph (stub)
        self.graph_widget = QtWidgets.QLabel()
        self.graph_widget.setStyleSheet("QLabel { background-color: #222; }")
        self.central_widget_layout.addWidget(self.graph_widget)

        # Control panel
        self.control_group = QtWidgets.QGroupBox()
        self.control_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        self.control_group_layout = QtWidgets.QHBoxLayout(self.control_group)
        self.central_widget_layout.addWidget(self.control_group)

        # Control run
        self.control_run = QtWidgets.QPushButton()
        self.control_run.setText("Run")
        self.control_run.setCheckable(True)
        self.control_run.clicked.connect(self._control_checkbox_run_event)
        self.control_group_layout.addWidget(self.control_run)

        # Control learn
        self.control_learn = QtWidgets.QPushButton()
        self.control_learn.setText("Learn")
        self.control_learn.setCheckable(True)
        self.control_learn.setEnabled(False)
        self.control_group_layout.addWidget(self.control_learn)

        # Control predicate
        self.control_predicate = QtWidgets.QPushButton()
        self.control_predicate.setText("Predicate")
        self.control_predicate.setCheckable(True)
        self.control_predicate.setEnabled(False)
        self.control_group_layout.addWidget(self.control_predicate)

        # Final logic
        self._fill_currencies_comboboxes()

    def _fill_currencies_comboboxes(self) -> None:
        for currency in base_currencies:
            self.base_currency.addItem(currency["id"])
        self.base_currency.setCurrentText("USD")
        for currency in crypto_currencies:
            self.crypto_currency.addItem(currency)
        self.crypto_currency.setCurrentText("BTC")

    def _control_checkbox_run_event(self, is_checked: bool) -> None:
        self.log(f"self._control_checkbox_run_event({is_checked=})")
        self.currencies_group.setEnabled(not is_checked)
        self.control_learn.setEnabled(is_checked)
        self.control_predicate.setEnabled(is_checked)
        if is_checked:
            price = client.get_spot_price(
                currency_pair=f"{self.crypto_currency.currentText()}-{self.base_currency.currentText()}"
            )["amount"]
            self.graph_widget.setText(price)
        else:
            self.graph_widget.setText("")
        print(self.size())
