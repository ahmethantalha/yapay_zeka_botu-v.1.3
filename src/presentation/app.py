import customtkinter as ctk
from src.core.config import AppConfig
from src.database.database import Database
from src.core.security import Security
from src.repositories.ai_config_repository import AIConfigRepository
from src.models.ai_config import AIConfig
from src.repositories.history_repository import HistoryRepository
from src.models.history import AnalysisHistory
from src.repositories.custom_analysis_repository import CustomAnalysisRepository  # YENİ!
from src.models.custom_analysis_type import CustomAnalysisType  # YENİ!
from src.services.ai_service_manager import AIServiceManager
from src.presentation.viewmodels.main_viewmodel import MainViewModel
from src.presentation.views.main_window import MainWindow

class Application:
    def __init__(self, config: AppConfig):
        self.config = config
        # Tesseract kurulumunu kontrol et
        self.setup_tesseract()  

        # Setup database
        self.db = Database(config)
        self.db.create_tables()
        self.session = self.db.get_session()
        
        # Setup security
        self.security = Security()
        
        # Setup repositories
        self.ai_config_repo = AIConfigRepository(self.session, AIConfig)
        self.history_repo = HistoryRepository(self.session, AnalysisHistory)
        self.custom_analysis_repo = CustomAnalysisRepository(self.session, CustomAnalysisType)  # YENİ!
        
        # Setup services
        self.ai_service_manager = AIServiceManager(self.ai_config_repo, self.security)
        
        # Setup viewmodels
        self.main_viewmodel = MainViewModel(self.ai_service_manager)
        self.main_viewmodel.history_repo = self.history_repo
        self.main_viewmodel.custom_analysis_repo = self.custom_analysis_repo  # YENİ!
        
        # Setup UI
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.main_window = MainWindow(self.main_viewmodel)
        # Set session to the main window and its components
        self.main_window.set_session(self.session)
        
        # Make session accessible
        self.main_window.session = self.session

    
    def run(self):
        """Start the application"""
        self.main_window.mainloop()


    @staticmethod
    def setup_tesseract():
        """Tesseract OCR ayarlarını yapılandır"""
        try:
            import pytesseract
            import os
            
            # Windows'ta Tesseract yolunu kontrol et
            if os.name == 'nt':
                # Ana Tesseract yolu
                tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                
                # Alternatif yollar
                alt_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    # Kullanıcı dizininde kurulu olabilir
                    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Tesseract-OCR', 'tesseract.exe')
                ]
                
                # Olası yolları kontrol et
                for path in alt_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        print(f"Tesseract bulundu: {path}")
                        return True
                
                print("Tesseract OCR bulunamadı. Görüntü analizi çalışmayabilir.")
                return False
            
            return True  # Windows dışındaki sistemlerde varsayılan yol kullanılır
        except ImportError:
            print("pytesseract modülü bulunamadı. Görüntü analizi çalışmayabilir.")
            return False


