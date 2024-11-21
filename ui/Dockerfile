FROM node:20-alpine AS build

ARG BACKEND_URL

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

ENV VITE_BACKEND_URL=$BACKEND_URL

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5000

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
