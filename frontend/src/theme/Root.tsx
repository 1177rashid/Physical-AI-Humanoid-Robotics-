import React from 'react';
import {UserPreferencesProvider} from '../utils/userPreferences';

// Default implementation, that you can customize
function Root({children}) {
  return (
    <UserPreferencesProvider>
      {children}
    </UserPreferencesProvider>
  );
}

export default Root;