export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
  get apiBaseUrl() {
    return this.apiUrl;
  }
};
