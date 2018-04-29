import { helper } from '@ember/component/helper';

export function humanizeDuration(params, hash) {
  if (!hash.end) {
    return "";
  }
  let duration_seconds = hash.end - hash.start;
  let days = Math.floor(duration_seconds / (24 * 60 * 60));
  duration_seconds %= 24 * 60 * 60;
  let hours = Math.floor(duration_seconds / (60 * 60));
  duration_seconds %= 60 * 60;
  let minutes = Math.floor(duration_seconds / 60);
  duration_seconds = Math.floor(duration_seconds % 60);

  let returned = `${duration_seconds}s`;

  if (hours || minutes) {
    returned = `${minutes}m ${returned}`;
  }
  if (hours || days) {
    returned = `${hours}h ${returned}`;
  }
  if (days) {
    returned = days + "d " + returned;
  }
  return returned;
}

export default helper(humanizeDuration);
