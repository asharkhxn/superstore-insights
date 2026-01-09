import { useState, useEffect } from "react";

interface FetchState<T> {
  data: T | null;
  loading: boolean; // true only when no data yet
  refreshing: boolean; // true when updating but keeping prior data rendered
  error: string | null;
}

type ParamValue = string | number | null | undefined | Array<string | number>;

interface FetchOptions {
  params?: Record<string, ParamValue>;
}

const serializeParams = (params?: Record<string, ParamValue>) => {
  if (!params) return "";

  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) return;

    if (Array.isArray(value)) {
      value.forEach((v) => searchParams.append(key, String(v)));
    } else {
      searchParams.set(key, String(value));
    }
  });

  const query = searchParams.toString();
  return query ? `?${query}` : "";
};

export function useFetch<T>(
  url: string,
  options?: FetchOptions
): FetchState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        setError(null);
        // only show primary loading when we have no data yet
        setLoading(data === null);
        setRefreshing(data !== null);

        const query = serializeParams(options?.params);
        const response = await fetch(`${url}${query}`);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (isMounted) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "An error occurred");
          // keep prior data to avoid flicker if we had any
        }
      } finally {
        if (isMounted) {
          setLoading(false);
          setRefreshing(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [url, JSON.stringify(options?.params || {})]);

  return { data, loading, refreshing, error };
}
