import React, {createContext, useContext, useEffect, useState} from 'react';

interface UserPreferences {
  fontSize: 'small' | 'normal' | 'large';
  theme: 'light' | 'dark';
  // Add more user preferences as needed
}

interface UserPreferencesContextType {
  preferences: UserPreferences;
  updatePreferences: (newPreferences: Partial<UserPreferences>) => void;
}

const UserPreferencesContext = createContext<UserPreferencesContextType | undefined>(undefined);

const UserPreferencesProvider: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [preferences, setPreferences] = useState<UserPreferences>({
    fontSize: 'normal',
    theme: 'light',
  });

  useEffect(() => {
    // Load preferences from localStorage on mount
    const savedPreferences = localStorage.getItem('userPreferences');
    if (savedPreferences) {
      try {
        setPreferences(JSON.parse(savedPreferences));
      } catch (e) {
        console.error('Failed to parse user preferences', e);
      }
    }
  }, []);

  const updatePreferences = (newPreferences: Partial<UserPreferences>) => {
    setPreferences(prev => {
      const updated = {...prev, ...newPreferences};
      // Save to localStorage
      localStorage.setItem('userPreferences', JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <UserPreferencesContext.Provider value={{preferences, updatePreferences}}>
      {children}
    </UserPreferencesContext.Provider>
  );
};

const useUserPreferences = () => {
  const context = useContext(UserPreferencesContext);
  if (context === undefined) {
    throw new Error('useUserPreferences must be used within a UserPreferencesProvider');
  }
  return context;
};

export {UserPreferencesProvider, useUserPreferences};
export type {UserPreferences};