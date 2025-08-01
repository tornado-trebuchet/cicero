export const environment = {
  production: true,
  apiUrl: 'PLACEHOLDER',
  get apiBaseUrl() {
    return this.apiUrl;
  }
};
