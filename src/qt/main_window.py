from parser import client, currencies

from PyQt6 import QtCore, QtWidgets


# noinspection PyUnresolvedReferences
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
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
        self.currencies_group.setStyleSheet("QComboBox { combobox-popup: 0; }")
        # Currency combobox
        self.currency = QtWidgets.QComboBox()
        self.currency.setMaxVisibleItems(20)
        self.currencies_layout.addWidget(self.currency)
        # '/' label between comboboxes
        label = QtWidgets.QLabel(" / ")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        )
        self.currencies_layout.addWidget(label)
        # Currency-base combobox
        self.currency_base = QtWidgets.QComboBox()
        self.currency_base.setMaxVisibleItems(20)
        self.currencies_layout.addWidget(self.currency_base)

        # Graph (stub)
        self.graph_widget = QtWidgets.QLabel()
        self.central_widget_layout.addWidget(self.graph_widget)
        self.graph_widget.setStyleSheet("QLabel { background-color: #222; }")

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

        # Final logic
        self._fill_currency_combobox()

    def _fill_currency_combobox(self) -> None:
        for currency in currencies:
            self.currency_base.addItem(currency["id"])
        self.currency_base.currentTextChanged.connect(self._change_currency_combobox_event)
        self.currency_base.setCurrentText("USD")

    def _change_currency_combobox_event(self, item) -> None:
        self.rates = client.get_exchange_rates(currency=item)["rates"]
        for rate in self.rates:
            self.currency.addItem(rate)
        self.currency.setCurrentText("BTC")
