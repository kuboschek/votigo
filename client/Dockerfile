FROM node:current-alpine as builder
WORKDIR /app
COPY package*.json .
RUN yarn install --immutable
COPY . .
RUN yarn run build

FROM node:current-alpine
WORKDIR /app
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]