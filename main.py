import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget,
                             QGroupBox, QFileDialog, QStatusBar, QProgressBar)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

# from Chat.server import server
# from Chat.client import client
class P2PFileShareApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2P File Sharing System")
        self.resize(900, 600)
        self.setMinimumSize(800, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # do section m divide -> chat aur file section
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # File operations section
        file_widget = QWidget()
        splitter.addWidget(file_widget)
        file_layout = QVBoxLayout(file_widget)
        
        # Create file section 
        file_section = self.create_file_section()
        file_layout.addWidget(file_section)
        
        # Chat section
        chat_widget = QWidget()
        splitter.addWidget(chat_widget)
        chat_layout = QVBoxLayout(chat_widget)
        
        # Create chat section 
        chat_section = self.create_chat_section()
        chat_layout.addWidget(chat_section)
        
        splitter.setSizes([450, 450])
        
        # bottom status 1-100% bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMaximumHeight(16)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
    def create_file_section(self):
        file_group = QGroupBox("P2P File Operations: ")
        layout = QVBoxLayout()
        
        # Selected file area
        file_selection_layout = QHBoxLayout()
        file_selection_layout.addWidget(QLabel("Selected File:"))
        
        self.selected_file_edit = QLineEdit()
        self.selected_file_edit.setReadOnly(True)
        file_selection_layout.addWidget(self.selected_file_edit)
        
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_file)
        file_selection_layout.addWidget(self.select_file_btn)
        
        layout.addLayout(file_selection_layout)
        
        file_ops_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload File")
        self.upload_btn.clicked.connect(self.upload_file)
        file_ops_layout.addWidget(self.upload_btn)
        
        # self.download_btn = QPushButton("Download File")
        # self.download_btn.clicked.connect(self.download_file)
        # file_ops_layout.addWidget(self.download_btn)
        
        self.share_btn = QPushButton("Share File")
        self.share_btn.clicked.connect(self.share_file)
        file_ops_layout.addWidget(self.share_btn)
        
        layout.addLayout(file_ops_layout)
        
        # Available files list
        layout.addWidget(QLabel("Available Shared Files:"))
        
        self.files_list = QListWidget()
        self.files_list.itemDoubleClicked.connect(self.file_selected)
        layout.addWidget(self.files_list)
        
        # Add some dummy files for demonstration
        # here file will listed

        transfer_layout = QHBoxLayout()
        transfer_layout.addWidget(QLabel("Transfer Status:"))
        self.transfer_status = QLabel("No active transfer")
        transfer_layout.addWidget(self.transfer_status)
        layout.addLayout(transfer_layout)
        
        file_group.setLayout(layout)
        return file_group
        
    def create_chat_section(self):
        chat_group = QGroupBox("Chat")
        layout = QVBoxLayout()
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Message input area
        message_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        message_layout.addWidget(self.message_input)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        message_layout.addWidget(self.send_btn)
        
        layout.addLayout(message_layout)
        
        # Connected peers
        peer_layout = QHBoxLayout()
        peer_layout.addStretch()
        layout.addLayout(peer_layout)
        
        chat_group.setLayout(layout)
        return chat_group
    
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File to Share", "", "All Files (*)")
        if file_name:
            self.selected_file_edit.setText(file_name)
            self.status_bar.showMessage(f"File selected: {file_name}")
    
    def upload_file(self):
        if not self.selected_file_edit.text():
            self.status_bar.showMessage("No file selected")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # real time while uploading file
        import time
        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents() 
            time.sleep(0.02) 
        
        file_name = self.selected_file_edit.text().split('/')[-1]
        self.files_list.addItem(file_name)
        self.status_bar.showMessage(f"File uploaded: {file_name}")
        self.progress_bar.setVisible(False)
        
        # Add message to chat
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.chat_display.append(f"[{timestamp}] You: Uploaded file '{file_name}'")
    
    # def download_file(self):
    #     if not self.files_list.currentItem():
    #         self.status_bar.showMessage("No file selected for download")
    #         return
            
    #     file_name = self.files_list.currentItem().text()
    #     save_path, _ = QFileDialog.getSaveFileName(self, "Save File", file_name, "All Files (*)")
        
    #     if save_path:
    #         # Simulating download process
    #         self.progress_bar.setVisible(True)
    #         self.progress_bar.setValue(0)
            
    #         # In a real app, you would use QThread for this operation
    #         import time
    #         for i in range(101):
    #             self.progress_bar.setValue(i)
    #             QApplication.processEvents()  # Keep UI responsive
    #             time.sleep(0.02)  # Simulate network delay
            
    #         self.status_bar.showMessage(f"File downloaded: {file_name}")
    #         self.progress_bar.setVisible(False)
            
    #         # Add message to chat
    #         timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
    #         self.chat_display.append(f"[{timestamp}] You: Downloaded file '{file_name}'")
    
    def share_file(self):
        if not self.selected_file_edit.text():
            self.status_bar.showMessage("No file selected to share")
            return
            
        file_name = self.selected_file_edit.text().split('/')[-1]
        
        self.status_bar.showMessage(f"File shared: {file_name}")
        
        # Add message to chatting section
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.chat_display.append(f"[{timestamp}] You: Shared file '{file_name}' with the network")
    
    def file_selected(self, item):
        self.status_bar.showMessage(f"Selected: {item.text()}")
    
    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
            self.chat_display.append(f"[{timestamp}] You: {message}")
            self.message_input.clear()
            
            # In a real app, this would send the message to peers
            # Simulate receiving a response
            import time
            QApplication.processEvents()
            time.sleep(1)
            # hardcoded message -> real message will be received from peer
            self.chat_display.append(f"[{timestamp}] Peer: I received your message!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern look across platforms
    
    window = P2PFileShareApp()
    window.show()
    
    sys.exit(app.exec_())