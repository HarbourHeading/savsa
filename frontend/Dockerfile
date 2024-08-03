FROM node:20-alpine AS builder

WORKDIR /frontend

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

FROM nginx:1.25.2-alpine-slim

COPY --from=builder frontend/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]