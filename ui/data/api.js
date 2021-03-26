import useSWR from "swr";

const root = "http://127.0.0.1:5000";
const fetcher = (...args) => fetch(...args).then((res) => res.json());

function fetchBase(url) {
  const { data, error } = useSWR(url, fetcher);

  return {
    data: data,
    isLoading: !error && !data,
    isError: error,
  };
}

export function allDataIDs() {
  return fetchBase(`${root}/data_ids`);
}

export function dbStats() {
  return fetchBase(`${root}/dbstats`);
}

export function records() {
  return fetchBase(`${root}/records`);
}

export function dataRecord(data_id) {
  return fetchBase(`${root}/records/${data_id}`);
}

export function dataStats(data_id) {
  return fetchBase(`${root}/stats/${data_id}`);
}
