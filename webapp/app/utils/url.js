export function normalize_id_from_url(raw_id) {
  let returned = raw_id.split("\x1B[")[0];
  return returned;
}
