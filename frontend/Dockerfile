# syntax=docker/dockerfile:1

FROM node:20

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Angular dev server port
EXPOSE 4200

# Start Angular dev server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]