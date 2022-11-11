import logging
from typing import List

import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets

from src import CUSTOM_LOG_LEVEL
from src.data import BASE_CURRENCIES, CRYPTO_CURRENCIES
from src.parser import parse_dataset
from src.uninn import learn, predicate


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log = lambda *args_, **kwargs_: logging.log(CUSTOM_LOG_LEVEL, *args_, **kwargs_)

        # Main window
        self.setWindowTitle("Crypto-predictor")
        self.setMinimumSize(600, 400)
        self.resize(900, 500)

        # Central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Currencies group
        self.currencies_group = QtWidgets.QGroupBox()
        self.currencies_group.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currencies_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)

        # Currencies comboboxes
        self.fiat_curr = QtWidgets.QComboBox(self.currencies_group)
        self.crypto_curr = QtWidgets.QComboBox(self.currencies_group)
        self.fiat_curr.setMaxVisibleItems(30)
        self.crypto_curr.setMaxVisibleItems(30)

        # Slash-label between comboboxes
        slash_label = QtWidgets.QLabel("  /  ", self.currencies_group)
        slash_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        slash_label.setMinimumWidth(30)
        slash_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)

        # Plot widget and item
        self.plot_item = pg.PlotItem()
        self.plot_item.setLabel("left", "Price")
        self.plot_item.setLabel("bottom", "Minutes")
        self.plot_item.addLegend()
        self.plot_widget = pg.PlotWidget(self.central_widget, plotItem=self.plot_item)
        self.plot_widget.setBackground(self.palette().color(QtGui.QPalette.ColorRole.Window))

        # Plot data items
        self.actual_price_data_item = pg.PlotDataItem(name="Actual price")
        self.predicated_price_data_item = pg.PlotDataItem(name="Predicated price")
        self.predicated_price_data_item.setPen(pg.mkPen(QtGui.QColor("red")))
        self.updated_price_data_item = pg.PlotDataItem(name="Updated price")
        self.updated_price_data_item.setPen(pg.mkPen(QtGui.QColor("blue")))
        self.plot_item.addItem(self.actual_price_data_item)
        self.plot_item.addItem(self.predicated_price_data_item)
        self.plot_item.addItem(self.updated_price_data_item)

        # Infinite line
        self.infinite_line = pg.InfiniteLine(0, pen=pg.mkPen(QtGui.QColor("dimgray")))

        # Control panel
        self.control_group = QtWidgets.QGroupBox()
        self.control_group.setMaximumHeight(60)

        # Control run
        self.control_run = QtWidgets.QPushButton()
        self.control_run.setText("Run")
        self.control_run.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.control_run.setCheckable(True)
        self.control_run.clicked.connect(self._control_run_event)

        # Control learn
        self.control_learn = QtWidgets.QPushButton()
        self.control_learn.setText("Learn")
        self.control_learn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.control_learn.setDisabled(True)
        self.control_learn.clicked.connect(self._control_learn_event)

        # Control predicate
        self.control_predicate = QtWidgets.QPushButton()
        self.control_predicate.setText("Predicate")
        self.control_predicate.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.control_predicate.setDisabled(True)
        self.control_predicate.clicked.connect(self._control_predicate_event)

        # Control update
        self.control_update = QtWidgets.QPushButton()
        self.control_update.setText("Update")
        self.control_update.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.control_update.setDisabled(True)
        self.control_update.clicked.connect(self._control_update_event)

        # Layouts
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_widget_layout.addWidget(self.currencies_group)
        self.central_widget_layout.addWidget(self.plot_widget)
        self.central_widget_layout.addWidget(self.control_group)

        self.currencies_layout = QtWidgets.QHBoxLayout(self.currencies_group)
        self.currencies_layout.addWidget(self.crypto_curr)
        self.currencies_layout.addWidget(slash_label)
        self.currencies_layout.addWidget(self.fiat_curr)

        self.control_group_layout = QtWidgets.QHBoxLayout(self.control_group)
        self.control_group_layout.addWidget(self.control_run)
        self.control_group_layout.addWidget(self.control_learn)
        self.control_group_layout.addWidget(self.control_predicate)
        self.control_group_layout.addWidget(self.control_update)

        # Final logic
        self._fill_currencies_comboboxes()

    def _fill_currencies_comboboxes(self) -> None:
        for currency in BASE_CURRENCIES:
            self.fiat_curr.addItem(currency)
        self.fiat_curr.setCurrentText("USD")

        for currency in CRYPTO_CURRENCIES:
            self.crypto_curr.addItem(currency)
        self.crypto_curr.setCurrentText("BTC")

    def _control_run_event(self, is_checked: bool) -> None:
        self.log(f"control_run_event: started with {is_checked=})")
        self.currencies_group.setDisabled(is_checked)
        self.control_learn.setEnabled(is_checked)
        self.control_update.setEnabled(is_checked)

        if not is_checked:
            self.actual_price_data_item.setData()
            self.plot_item.removeItem(self.infinite_line)
            self.predicated_price_data_item.setData()
            self.updated_price_data_item.setData()
            return

        self.rates, self.datetimes = parse_dataset(f"{self.crypto_curr.currentText()}-{self.fiat_curr.currentText()}")
        self.last_time = self.datetimes[-1]
        self.times: List[float] = [(dataset_dt - self.last_time).total_seconds() / 60 for dataset_dt in self.datetimes]
        self.period_minutes = abs(self.times[-2])
        self.actual_price_data_item.setData(self.times, self.rates)
        self.plot_item.addItem(self.infinite_line)
        self.log(f"control_run_event: set params {self.last_time=}, {self.period_minutes=}, {self.times=}")

    def _control_learn_event(self) -> None:
        self.log("control_learn_event: started")
        learn(self.rates, 300)
        self.control_predicate.setEnabled(True)
        self.log("control_learn_event: finished")

    def _control_predicate_event(self) -> None:
        n = 20
        self.log(f"control_learn_event: started with {n=}")
        data = predicate(self.rates, n)
        times = [i * self.period_minutes for i in range(0, n + 1)]

        self.predicated_price_data_item.setData(times, data)
        self.control_predicate.setDisabled(True)

    def _control_update_event(self) -> None:
        self.log("control_update_event: started")
        rates, datetimes = parse_dataset(f"{self.crypto_curr.currentText()}-{self.fiat_curr.currentText()}")
        try:
            last_i = datetimes.index(self.last_time)
        except ValueError:
            self.log("control_update_event: No last_time in parsed data")
            return
        rates = rates[last_i:]
        datetimes = datetimes[last_i:]
        self.log(f"control_update_event: update {len(datetimes) - 1} new data {datetimes=}")
        times: List[float] = [(dataset_dt - self.last_time).total_seconds() / 60 for dataset_dt in datetimes]
        self.updated_price_data_item.setData(times, rates)
