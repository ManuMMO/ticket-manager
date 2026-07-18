# Etapa 1: build
FROM node:20 AS build

WORKDIR /usr/src/app

RUN corepack enable
RUN corepack prepare pnpm@9.1.0 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .

ARG API_BASE_URL
ENV API_BASE_URL=$API_BASE_URL

RUN pnpm generate

# Etapa 2: servir
FROM node:20-alpine

WORKDIR /usr/src/app

RUN npm install -g serve

COPY --from=build /usr/src/app/.output/public ./

EXPOSE 3000

CMD ["serve", "-s", ".", "-l", "3000"]