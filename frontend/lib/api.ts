import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: { "Content-Type": "application/json" },
});

export const analyzeUser = (github_username: string) =>
  api.post("/users/analyze/", { github_username });

export const getUser = (username: string) =>
  api.get(`/users/${username}/`);

export const analyzeRepo = (full_name: string) =>
  api.post("/repositories/analyze/", { full_name });

export const analyzeIssues = (full_name: string) =>
  api.post("/issues/analyze/", { full_name });

export const getRecommendations = (github_username: string, full_name?: string) =>
  api.post("/matching/recommend/", { github_username, full_name });

export const submitGrowth = (github_username: string, pr_url: string) =>
  api.post("/matching/growth/", { github_username, pr_url });

export default api;