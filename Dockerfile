# build stage
# Use the node image from official Docker Hub
FROM node:18-alpine as build-stage
# set the working directory
WORKDIR /app
# Copy the working directory in the container
COPY package*.json ./
# Install the project dependencies
RUN npm install
# Copy the rest of the project files to the container
COPY . .
# Build the Vue.js application to the production mode to dist folder
RUN npm run build

# production stage
# Use the lightweight Nginx image from the previous stage for the nginx container
FROM nginx:stable-alpine as production-stage
# Copy the build application from the previous stage to the Nginx container
COPY --from=build-stage /app/dist /usr/share/nginx/html
# Expose the port 2302
EXPOSE 2302
# Start Nginx to serve the application
CMD ["nginx", "-g", "daemon off;"]