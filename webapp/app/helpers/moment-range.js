import { helper } from '@ember/component/helper';

/* global moment */

export function momentRange(params, opts) {
  if (opts.start_time === undefined) {
    return "-";
  }

  if (!opts.end_time) {
    return "Started " + moment.unix(opts.start_time).calendar();
  }

  let range = moment.unix(opts.start_time).twix(moment.unix(opts.end_time));

  if (opts.expanded) {
    return range.simpleFormat("YYYY/MM/DD HH:mm:ss");
  }
  return range.format();
}

export default helper(momentRange);
