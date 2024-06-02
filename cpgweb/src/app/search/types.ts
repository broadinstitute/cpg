export type TFacets = {
  value: string;
  highlighted: string;
  count: number;
};

export type TFacetResponse = {
  exhaustiveFacetsCount: boolean;
  facets: TFacets;
  processingTimeMS: number;
};

export type TSearchResult = {
  hits: THit[];
  nbHits: number;
  page: number;
  nbPages: number;
  hitsPerPage: number;
  exhaustiveNbHits: boolean;
  exhaustiveTypo: boolean;
  exhaustive: TExhaustive;
  query: string;
  params: string;
  renderingContent: TRenderingContent;
  processingTimeMS: number;
  processingTimingsMS: TProcessingTimingsMs;
  serverTimeMS: number;
};

export type THit = {
  PlateName?: string;
  Row?: string;
  Col?: number;
  Well?: string;
  Name?: string;
  PublicID?: string;
  Vector: any;
  Transcript: any;
  Symbol: any;
  x_mutation_status: any;
  NCBIGeneID: any;
  OtherDescriptions: any;
  InsertLength: any;
  pert_type?: string;
  project_id: string;
  objectID: string;
  _highlightResult: THighlightResult;
  Assay_Plate_Barcode: any;
  Plate_Map_Name?: string;
};

export type THighlightResult = {
  PlateName?: TPlateName;
  Row?: TRow;
  Col?: TCol;
  Well?: TWell;
  Name?: TName;
  PublicID?: TPublicId;
  pert_type?: TPertType;
  project_id: TProjectId;
  Assay_Plate_Barcode?: TAssayPlateBarcode;
  Plate_Map_Name?: TPlateMapName;
};

export type TPlateName = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TRow = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TCol = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TWell = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TName = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TPublicId = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TPertType = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TProjectId = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TAssayPlateBarcode = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TPlateMapName = {
  value: string;
  matchLevel: string;
  matchedWords: any[];
};

export type TExhaustive = {
  nbHits: boolean;
  typo: boolean;
};

export type TRenderingContent = {};

export type TProcessingTimingsMs = {
  _request: Request;
  getIdx: TGetIdx;
  total: number;
};

export type TRequest = {
  roundTrip: number;
};

export type TGetIdx = {
  load: TLoad;
  total: number;
};

export type TLoad = {
  total: number;
};
