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

test("expect update table to render tablebody", () => {
  let testData = [{
      "uid": "auid",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a translation"
    },
    {
      "uid": "auisd",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a bigger translation"
    },
    {
      "uid": "auid",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a"
    },
    {
      "uid": "auid",
      "state": "completed",
      "text_to_translate": "some test text",
      "translation": "a huge translation here"
    }
  ]


const expectSorted =[{
      "state": "completed",
      "text_to_translate": "some test text",
     "translation": "updated translation",
     "translation": "a huge translation here",
     "uid": "auid",
   },
    {
     "state": "completed",
     "text_to_translate": "some test text",
     "translation": "a bigger translation",
     "uid": "auisd",
   },
    {
     "state": "completed",
     "text_to_translate": "some test text",
     "translation": "a translation",
     "uid": "auid",
   },{
     "state": "completed",
     "text_to_translate": "some test text",
     "translation": "a",
      "uid": "auid",
    },
  ]

  table.setTabledata(testData);
  expect(table.sortTable(testData)).toEqual(expectSorted);
});


