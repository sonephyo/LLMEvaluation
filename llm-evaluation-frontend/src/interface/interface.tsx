export interface PromptInterface {
  systemPrompt: string;
  contentPrompt: string;
}

export interface ResultResponesInterface {
  data: LLMResponse[];
}

export interface LLMResponse {
  systemPrompt: string;
  response: string;
  contentPrompt: string;
  aiModel: string;
}

export interface LLMResponseData {
    systemPrompt: string;
    response: string;
    contentPrompt: string;
    aiModel: string;
    score: string;
}