class LocalForecast: 
    def __init__(self, risk_type, risk_level, risk_location): 
        self._risk_type = risk_type 
        self._risk_level = risk_level 
        self._risk_location = risk_location 
    
    def get_risk_type(self): 
        return self._risk_type 
    
    def get_risk_level(self): 
        return self._risk_level 
    
    def get_city(self): 
        return self._risk_location