const table = require("../../challenge/static/table");

test("expect load table to render tablebody", () => {
  let testData = [{
      "uid": "auid",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a translation"
    },]
  let rendered = table.loadTableData(testData);
  expect(rendered).toBe("<tr><td>auid</td><td>completed</td><td>some test text</td><td>a translation</td></tr>");
});

test("expect update table to render tablebody", () => {
  let testData = [{
      "uid": "auid",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a translation"
    },]
  table.setTabledata(testData);
  table.updateTranslationOnTable('auid','updated translation');
  expect(table.getTableData()).toEqual([{"state": "completed", "text_to_translate": "some test text", "translation": "updated translation", "uid": "auid"}]);
});

