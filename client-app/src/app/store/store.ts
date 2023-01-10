import { createContext, useContext } from "react"
import ModelStore from "./modelStore";

interface Store {
    modelStore: ModelStore
}

export const store: Store = {
    modelStore: new ModelStore(),
}
export const StoreContext = createContext(store);

export function useStore() {
    return useContext(StoreContext);
}