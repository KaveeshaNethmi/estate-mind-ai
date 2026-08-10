export interface ChatRequest {
  question: string;
  top_k?: number;

  conversation_id?: string | null;

  city?: string | null;
  area?: string | null;
  development?: string | null;
  property_type?: string | null;
  max_price?: number | null;
  min_bedrooms?: number | null;
}

export interface SearchState {
  city?: string | null;
  area?: string | null;
  development?: string | null;
  property_type?: string | null;
  max_price?: number | null;
  min_bedrooms?: number | null;

  [key: string]: unknown;
}

export interface ChatMetadata {
  conversation_id: string;
  rewritten_query: string;
  search_state: SearchState;
  reference_detected: boolean;
  reused_previous_results: boolean;
}

export interface ChatCitation {
  [key: string]: unknown;
}

export interface ChatConfidence {
    score: number;
    level: string;
    reasons: string[];
}

export interface PropertySource {
  [key: string]: unknown;
}

export interface ChatCompleteData {
  answer: string;
  citations: ChatCitation[];
  confidence: ChatConfidence;
  sources: PropertySource[];
}

export interface ChatErrorData {
  message: string;
  details?: string;
}

export type ChatStreamEvent =
  | {
      type: "metadata";
      data: ChatMetadata;
    }
  | {
      type: "token";
      data: {
        content: string;
      };
    }
  | {
      type: "complete";
      data: ChatCompleteData;
    }
  | {
      type: "error";
      data: ChatErrorData;
    };

export type ChatRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;

  isStreaming?: boolean;

  citations?: ChatCitation[];
  confidence?: number;

//   confidence?: number;
  sources?: PropertySource[];
}