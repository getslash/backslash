import { helper } from "@ember/component/helper";

export function statusToBrand(params /*, hash*/) {
  let status = params[0];
  if (!status) {
    return "secondary";
  }
  switch (status.toLowerCase()) {
    case "success":
      return "success";
    case "error":
    case "failure":
      return "danger";
    case "skipped":
    case "skip":
      return "warning";
    default:
      return "secondary";
  }
}

export default helper(statusToBrand);
