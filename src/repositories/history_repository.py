import pickle
from typing import List, Optional
from .base_repository import BaseRepository
from src.models.history import AnalysisHistory
from src.services.file_processing.result_manager import ProcessingResult

class HistoryRepository(BaseRepository[AnalysisHistory]):
    """Repository for managing analysis history"""
    
    def save_analysis(self, result: ProcessingResult, provider: str) -> AnalysisHistory:
        """Save analysis result to history"""
        # Create summary (first 200 characters)
        summary = result.analyzed_text[:200] + "..." if len(result.analyzed_text) > 200 else result.analyzed_text
        
        # Determine file type from file name
        import os
        file_type = os.path.splitext(result.file_name)[1]
        
        # Create history entry
        history = AnalysisHistory(
            file_name=result.file_name,
            file_type=file_type,
            analysis_type=result.analysis_type,
            provider=provider,
            summary=summary,
            result_data=pickle.dumps(result)
        )
        
        return self.create(history)
    
    def get_recent_analyses(self, limit: int = 20) -> List[AnalysisHistory]:
        """Get recent analyses"""
        return self.session.query(AnalysisHistory)\
            .order_by(AnalysisHistory.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_by_file_type(self, file_type: str, limit: int = 20) -> List[AnalysisHistory]:
        """Get analyses by file type"""
        return self.session.query(AnalysisHistory)\
            .filter(AnalysisHistory.file_type == file_type)\
            .order_by(AnalysisHistory.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_by_analysis_type(self, analysis_type: str, limit: int = 20) -> List[AnalysisHistory]:
        """Get analyses by analysis type"""
        return self.session.query(AnalysisHistory)\
            .filter(AnalysisHistory.analysis_type == analysis_type)\
            .order_by(AnalysisHistory.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_by_provider(self, provider: str, limit: int = 20) -> List[AnalysisHistory]:
        """Get analyses by AI provider"""
        return self.session.query(AnalysisHistory)\
            .filter(AnalysisHistory.provider == provider)\
            .order_by(AnalysisHistory.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_result(self, history_id: int) -> Optional[ProcessingResult]:
        """Get full result data from history entry"""
        history = self.get_by_id(history_id)
        if history and history.result_data:
            return pickle.loads(history.result_data)
        return None
    
    def delete(self, history_id: int) -> bool:
        """Delete analysis history by ID"""
        try:
            # Get the history item
            history = self.session.query(AnalysisHistory).get(history_id)
            
            if history:
                # Delete from database
                self.session.delete(history)
                self.session.commit()
                return True
            return False
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Geçmiş silinirken hata oluştu: {str(e)}")