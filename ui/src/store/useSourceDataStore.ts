import { create } from "zustand";
import { immer } from "zustand/middleware/immer"
import { SourceData } from "@/shared/interfaces/sourceData";

type SetSourceData = {
    sourceDataId: string,
    sourceData: Record<string, any>[]
}

type SourceDataAction = {
    setSourceData: (sourceDataPayload: SetSourceData) => void
}

type SourceDataState = {
    sourceData: SourceData
}

export const useSourceDataStore = create<SourceDataState & SourceDataAction>()(
  immer((set) => ({
    sourceData: {}, // getting error here
    setSourceData: ({ sourceDataId, sourceData }) => {
      set((state) => {
        if(sourceDataId){
            state.sourceData[sourceDataId] = sourceData;
        }
      });
    },
  }))
);
