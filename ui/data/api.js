import useSWR from "swr";

const root = process.env.NEXT_PUBLIC_API_URL;
console.log(root)
const fetcher = (...args) => fetch(...args).then((res) => res.json());

function fetchBase(url) {
    const {data, error} = useSWR(url, fetcher);

    return {
        data: data,
        isLoading: !error && !data,
        isError: error,
    };
}

export function allDataIDs() {
    console.log(`${root}/data_ids`)
    return fetchBase(`${root}/data_ids`);
}

export function dbStats() {
    console.log(`${root}/dbstats`)
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

export function roiMeta(data_id) {
    return fetchBase(`${root}/roi/${data_id}`);
}

export function cellInfo(roi_id) {
    return fetchBase(`${root}/cell_info/${roi_id}`);
}

export function expInfo(roi_id, marker) {
    return fetchBase(`${root}/cell_exp/${roi_id}/${marker}`);
}
