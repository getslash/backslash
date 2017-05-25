import Ember from "ember";

export function formatTestName(params, hash) {
  let [info] = params;
  let returned = "";

  if (info.getProperties !== undefined) {
    info = info.getProperties("file_name", "class_name", "name");
  }

  if (hash.with_filename === undefined || hash.with_filename) {
    returned += info.file_name + ":";
  }
  let class_name = info.class_name;
  if (
    class_name &&
    (class_name.indexOf("(") === -1 || class_name.endsWith(")"))
  ) {
    returned += info.class_name + ".";
  }
  returned += info.name;
  return returned;
}

export default Ember.Helper.helper(formatTestName);
