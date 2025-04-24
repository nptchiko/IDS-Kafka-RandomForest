import { createContext, ReactNode, useContext, useState } from "react";

type Log = { id: string; protocol: string; status: string };
type Status = { id: string; status: string };
type MissedByte = { id: string; time: string; missed_bytes: number };
type TlsPie = { id: string; name: string; value: number };

type AppContextType = {
    logsData: Log[];
    setLogsData: (logs: Log[]) => void;

    statusInfo: Status | null;
    setStatusInfo: (status: Status | null) => void;

    missedBytesData: MissedByte[];
    setMissedBytesData: (data: MissedByte[]) => void;

    tlsPieData: TlsPie[];
    setTlsPieData: (data: TlsPie[]) => void;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider = ({ children }: { children: ReactNode }) => {
    const [logsData, setLogsData] = useState<Log[]>([]);
    const [statusInfo, setStatusInfo] = useState<Status | null>(null);
    const [missedBytesData, setMissedBytesData] = useState<MissedByte[]>([]);
    const [tlsPieData, setTlsPieData] = useState<TlsPie[]>([]);

    return (
        <AppContext.Provider value={{
            logsData, setLogsData,
            statusInfo, setStatusInfo,
            missedBytesData, setMissedBytesData,
            tlsPieData, setTlsPieData
        }}>
            {children}
        </AppContext.Provider>
    );
}

export const useAppContext = () => {
    const ctx = useContext(AppContext);
    if (!ctx) throw new Error("useAppContext must be used inside <AppProvider>");
    return ctx;
  };