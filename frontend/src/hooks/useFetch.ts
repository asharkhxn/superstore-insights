import { useState, useEffect, useCallback } from "react";

interface FetchState<T> {
  data: T | null;
  loading: boolean; // true only when no data yet
  refreshing: boolean; // true when updating but keeping prior data rendered
  error: ApiError | null;
  retry: () => void; // function to retry the failed request
}

export interface ApiError {
  message: string;
  code: number | null;
  type: "network" | "server" | "client" | "unknown";
  isRetryable: boolean;
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

// Map HTTP status codes to user-friendly messages
const getErrorMessage = (status: number): string => {
  const errorMessages: Record<number, string> = {
    400: "Invalid request. Please check your filters and try again.",
    401: "Authentication required. Please log in.",
    403: "Access denied. You don't have permission to view this data.",
    404: "Data not found. The requested resource doesn't exist.",
    408: "Request timed out. Please try again.",
    429: "Too many requests. Please wait a moment and try again.",
    500: "Server error. Our team has been notified.",
    502: "Service temporarily unavailable. Please try again shortly.",
    503: "Data source is currently unavailable. Please try again later.",
    504: "Gateway timeout. The server took too long to respond.",
  };
  return (
    errorMessages[status] || `An unexpected error occurred (Error ${status})`
  );
};

// Parse error response and create structured error object
const parseError = async (response: Response): Promise<ApiError> => {
  const status = response.status;
  let message = getErrorMessage(status);

  // Try to get more specific error from response body
  try {
    const errorBody = await response.json();
    if (errorBody.detail) {
      message =
        typeof errorBody.detail === "string" ? errorBody.detail : message;
    }
  } catch {
    // Use default message if body parsing fails
  }

  const isRetryable = [408, 429, 500, 502, 503, 504].includes(status);
  const type: ApiError["type"] = status >= 500 ? "server" : "client";

  return { message, code: status, type, isRetryable };
};

// Handle network and fetch errors
const createNetworkError = (err: Error): ApiError => {
  const isNetworkError =
    err.message.includes("Failed to fetch") ||
    err.message.includes("NetworkError") ||
    err.message.includes("Network request failed") ||
    err.name === "TypeError";

  if (isNetworkError) {
    return {
      message:
        "Unable to connect to the server. Please check your internet connection.",
      code: null,
      type: "network",
      isRetryable: true,
    };
  }

  return {
    message: err.message || "An unexpected error occurred",
    code: null,
    type: "unknown",
    isRetryable: true,
  };
};

export function useFetch<T>(
  url: string,
  options?: FetchOptions
): FetchState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchData = useCallback(
    async (isMountedRef: { current: boolean }) => {
      try {
        setError(null);
        // only show primary loading when we have no data yet
        setLoading(data === null);
        setRefreshing(data !== null);

        const query = serializeParams(options?.params);
        const response = await fetch(`${url}${query}`);

        if (!response.ok) {
          const apiError = await parseError(response);
          throw apiError;
        }

        const result = await response.json();

        if (isMountedRef.current) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (isMountedRef.current) {
          if ((err as ApiError).type) {
            // Already parsed API error
            setError(err as ApiError);
          } else {
            // Network or unknown error
            setError(createNetworkError(err as Error));
          }
        }
      } finally {
        if (isMountedRef.current) {
          setLoading(false);
          setRefreshing(false);
        }
      }
    },
    [url, options?.params, data]
  );

  // Retry function that can be called by components
  const retry = useCallback(() => {
    setRetryCount((c) => c + 1);
  }, []);

  useEffect(() => {
    const isMountedRef = { current: true };
    fetchData(isMountedRef);

    return () => {
      isMountedRef.current = false;
    };
  }, [url, JSON.stringify(options?.params || {}), retryCount]);

  return { data, loading, refreshing, error, retry };
}
