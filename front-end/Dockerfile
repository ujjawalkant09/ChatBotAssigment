# Dockerfile for React frontend
FROM node:18 AS build

# Set working directory
WORKDIR /front-end

# Install dependencies and build
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve the app with nginx
FROM nginx:alpine
COPY --from=build /front-end/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
