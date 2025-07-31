export const environment = {
  production: true,
  apiUrl: 'https://your-production-domain.com',
  get apiBaseUrl() {
    return this.apiUrl;
  }
};
