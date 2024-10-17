import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from 'react';
import { useWindowSize } from 'usehooks-ts';

// Define the type for the Layout context
interface LayoutContextType {
  isSidebarOpen: boolean;
  setSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
  isGraphbarOpen: boolean;
  setGraphbarOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

// Create the Layout context
const LayoutContext = createContext<LayoutContextType | undefined>(undefined);

// Define the LayoutProvider component
export const LayoutProvider = ({ children }: { children: ReactNode }) => {
  const { width = 0 } = useWindowSize();
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [isGraphbarOpen, setGraphbarOpen] = useState(false);

  useEffect(() => {
    // Close the sidebar if the window width is less than 768px
    if (width < 768) {
      setSidebarOpen(false);
      setGraphbarOpen(false);
    }
  }, [width]);

  return (
    <LayoutContext.Provider
      value={{
        isSidebarOpen,
        setSidebarOpen,
        isGraphbarOpen,
        setGraphbarOpen,
      }}
    >
      {children}
    </LayoutContext.Provider>
  );
};

// Custom hook to use the Layout context
export const useLayout = () => {
  const context = useContext(LayoutContext);
  if (context === undefined) {
    throw new Error('useLayout must be used within a LayoutProvider');
  }
  return context;
};
