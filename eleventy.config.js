export default function (eleventyConfig) {
  // Site-wide static assets → /assets/...
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Art-directed articles ship their own assets alongside their page.
  // Anything under an article's assets/ folder is copied as-is.
  eleventyConfig.addPassthroughCopy("src/reviews/**/assets/**");
  eleventyConfig.addPassthroughCopy("src/essays/**/assets/**");

  // "Jul 2026" for cards, "July 10, 2026" for bylines
  eleventyConfig.addFilter("cardDate", (d) =>
    new Intl.DateTimeFormat("en", { month: "short", year: "numeric", timeZone: "UTC" }).format(d)
  );
  eleventyConfig.addFilter("bylineDate", (d) =>
    new Intl.DateTimeFormat("en", { dateStyle: "long", timeZone: "UTC" }).format(d)
  );
  eleventyConfig.addFilter("limit", (arr, n) => arr.slice(0, n));

  // Newest first — used everywhere content is listed
  eleventyConfig.addCollection("reviewsLatest", (api) =>
    api.getFilteredByTag("review").reverse()
  );
  eleventyConfig.addCollection("essaysLatest", (api) =>
    api.getFilteredByTag("essay").reverse()
  );
  // Most recent article marked `featured: true` takes the homepage hero
  eleventyConfig.addCollection("featured", (api) =>
    api.getAll().filter((p) => p.data.featured).sort((a, b) => a.date - b.date)
  );

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts",
    },
  };
}
