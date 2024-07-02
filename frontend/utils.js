export const getImageUrl = (path) => {  // Scalable way to get an image url
    return new URL(`/src/assets/${path}`, import.meta.url).href;
};
