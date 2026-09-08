//#region src/qss.ts
/**
* Program is a reimplementation of the `qss` package:
* Copyright (c) Luke Edwards luke.edwards05@gmail.com, MIT License
* https://github.com/lukeed/qss/blob/master/license.md
*
* This reimplementation uses modern browser APIs
* (namely URLSearchParams) and TypeScript while still
* maintaining the original functionality and interface.
*
* Update: this implementation has also been mangled to
* fit exactly our use-case (single value per key in encoding).
*/
/**
* Encodes an object into a query string.
* @param obj - The object to encode into a query string.
* @param stringify - An optional custom stringify function.
* @returns The encoded query string.
* @example
* ```
* // Example input: encode({ token: 'foo', key: 'value' })
* // Expected output: "token=foo&key=value"
* ```
*/
function encode(obj, stringify = String) {
	const result = new URLSearchParams();
	for (const key in obj) {
		const val = obj[key];
		if (val !== void 0) result.set(key, stringify(val));
	}
	return result.toString();
}
/**
* Converts a string value to its appropriate type (string, number, boolean).
* @param mix - The string value to convert.
* @returns The converted value.
* @example
* // Example input: toValue("123")
* // Expected output: 123
*/
function toValue(str) {
	if (!str) return "";
	if (str === "false") return false;
	if (str === "true") return true;
	return +str * 0 === 0 && +str + "" === str ? +str : str;
}
/**
* Decodes a query string into an object.
* @param str - The query string to decode.
* @returns The decoded key-value pairs in an object format.
* @example
* // Example input: decode("token=foo&key=value")
* // Expected output: { "token": "foo", "key": "value" }
*/
function decode(str) {
	const searchParams = new URLSearchParams(str);
	const result = Object.create(null);
	for (const [key, value] of searchParams.entries()) {
		const previousValue = result[key];
		if (previousValue == null) result[key] = toValue(value);
		else if (Array.isArray(previousValue)) previousValue.push(toValue(value));
		else result[key] = [previousValue, toValue(value)];
	}
	return result;
}
//#endregion
export { decode, encode };

                               
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicXNzLmpzIiwibmFtZXMiOltdLCJzb3VyY2VzIjpbIi4uLy4uL3NyYy9xc3MudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBQcm9ncmFtIGlzIGEgcmVpbXBsZW1lbnRhdGlvbiBvZiB0aGUgYHFzc2AgcGFja2FnZTpcbiAqIENvcHlyaWdodCAoYykgTHVrZSBFZHdhcmRzIGx1a2UuZWR3YXJkczA1QGdtYWlsLmNvbSwgTUlUIExpY2Vuc2VcbiAqIGh0dHBzOi8vZ2l0aHViLmNvbS9sdWtlZWQvcXNzL2Jsb2IvbWFzdGVyL2xpY2Vuc2UubWRcbiAqXG4gKiBUaGlzIHJlaW1wbGVtZW50YXRpb24gdXNlcyBtb2Rlcm4gYnJvd3NlciBBUElzXG4gKiAobmFtZWx5IFVSTFNlYXJjaFBhcmFtcykgYW5kIFR5cGVTY3JpcHQgd2hpbGUgc3RpbGxcbiAqIG1haW50YWluaW5nIHRoZSBvcmlnaW5hbCBmdW5jdGlvbmFsaXR5IGFuZCBpbnRlcmZhY2UuXG4gKlxuICogVXBkYXRlOiB0aGlzIGltcGxlbWVudGF0aW9uIGhhcyBhbHNvIGJlZW4gbWFuZ2xlZCB0b1xuICogZml0IGV4YWN0bHkgb3VyIHVzZS1jYXNlIChzaW5nbGUgdmFsdWUgcGVyIGtleSBpbiBlbmNvZGluZykuXG4gKi9cblxuLyoqXG4gKiBFbmNvZGVzIGFuIG9iamVjdCBpbnRvIGEgcXVlcnkgc3RyaW5nLlxuICogQHBhcmFtIG9iaiAtIFRoZSBvYmplY3QgdG8gZW5jb2RlIGludG8gYSBxdWVyeSBzdHJpbmcuXG4gKiBAcGFyYW0gc3RyaW5naWZ5IC0gQW4gb3B0aW9uYWwgY3VzdG9tIHN0cmluZ2lmeSBmdW5jdGlvbi5cbiAqIEByZXR1cm5zIFRoZSBlbmNvZGVkIHF1ZXJ5IHN0cmluZy5cbiAqIEBleGFtcGxlXG4gKiBgYGBcbiAqIC8vIEV4YW1wbGUgaW5wdXQ6IGVuY29kZSh7IHRva2VuOiAnZm9vJywga2V5OiAndmFsdWUnIH0pXG4gKiAvLyBFeHBlY3RlZCBvdXRwdXQ6IFwidG9rZW49Zm9vJmtleT12YWx1ZVwiXG4gKiBgYGBcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGVuY29kZShcbiAgb2JqOiBSZWNvcmQ8c3RyaW5nLCBhbnk+LFxuICBzdHJpbmdpZnk6ICh2YWx1ZTogYW55KSA9PiBzdHJpbmcgPSBTdHJpbmcsXG4pOiBzdHJpbmcge1xuICBjb25zdCByZXN1bHQgPSBuZXcgVVJMU2VhcmNoUGFyYW1zKClcblxuICBmb3IgKGNvbnN0IGtleSBpbiBvYmopIHtcbiAgICBjb25zdCB2YWwgPSBvYmpba2V5XVxuICAgIGlmICh2YWwgIT09IHVuZGVmaW5lZCkge1xuICAgICAgcmVzdWx0LnNldChrZXksIHN0cmluZ2lmeSh2YWwpKVxuICAgIH1cbiAgfVxuXG4gIHJldHVybiByZXN1bHQudG9TdHJpbmcoKVxufVxuXG4vKipcbiAqIENvbnZlcnRzIGEgc3RyaW5nIHZhbHVlIHRvIGl0cyBhcHByb3ByaWF0ZSB0eXBlIChzdHJpbmcsIG51bWJlciwgYm9vbGVhbikuXG4gKiBAcGFyYW0gbWl4IC0gVGhlIHN0cmluZyB2YWx1ZSB0byBjb252ZXJ0LlxuICogQHJldHVybnMgVGhlIGNvbnZlcnRlZCB2YWx1ZS5cbiAqIEBleGFtcGxlXG4gKiAvLyBFeGFtcGxlIGlucHV0OiB0b1ZhbHVlKFwiMTIzXCIpXG4gKiAvLyBFeHBlY3RlZCBvdXRwdXQ6IDEyM1xuICovXG5mdW5jdGlvbiB0b1ZhbHVlKHN0cjogdW5rbm93bikge1xuICBpZiAoIXN0cikgcmV0dXJuICcnXG5cbiAgaWYgKHN0ciA9PT0gJ2ZhbHNlJykgcmV0dXJuIGZhbHNlXG4gIGlmIChzdHIgPT09ICd0cnVlJykgcmV0dXJuIHRydWVcbiAgcmV0dXJuICtzdHIgKiAwID09PSAwICYmICtzdHIgKyAnJyA9PT0gc3RyID8gK3N0ciA6IHN0clxufVxuLyoqXG4gKiBEZWNvZGVzIGEgcXVlcnkgc3RyaW5nIGludG8gYW4gb2JqZWN0LlxuICogQHBhcmFtIHN0ciAtIFRoZSBxdWVyeSBzdHJpbmcgdG8gZGVjb2RlLlxuICogQHJldHVybnMgVGhlIGRlY29kZWQga2V5LXZhbHVlIHBhaXJzIGluIGFuIG9iamVjdCBmb3JtYXQuXG4gKiBAZXhhbXBsZVxuICogLy8gRXhhbXBsZSBpbnB1dDogZGVjb2RlKFwidG9rZW49Zm9vJmtleT12YWx1ZVwiKVxuICogLy8gRXhwZWN0ZWQgb3V0cHV0OiB7IFwidG9rZW5cIjogXCJmb29cIiwgXCJrZXlcIjogXCJ2YWx1ZVwiIH1cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGRlY29kZShzdHI6IGFueSk6IGFueSB7XG4gIGNvbnN0IHNlYXJjaFBhcmFtcyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoc3RyKVxuXG4gIGNvbnN0IHJlc3VsdDogUmVjb3JkPHN0cmluZywgdW5rbm93bj4gPSBPYmplY3QuY3JlYXRlKG51bGwpXG5cbiAgZm9yIChjb25zdCBba2V5LCB2YWx1ZV0gb2Ygc2VhcmNoUGFyYW1zLmVudHJpZXMoKSkge1xuICAgIGNvbnN0IHByZXZpb3VzVmFsdWUgPSByZXN1bHRba2V5XVxuICAgIGlmIChwcmV2aW91c1ZhbHVlID09IG51bGwpIHtcbiAgICAgIHJlc3VsdFtrZXldID0gdG9WYWx1ZSh2YWx1ZSlcbiAgICB9IGVsc2UgaWYgKEFycmF5LmlzQXJyYXkocHJldmlvdXNWYWx1ZSkpIHtcbiAgICAgIHByZXZpb3VzVmFsdWUucHVzaCh0b1ZhbHVlKHZhbHVlKSlcbiAgICB9IGVsc2Uge1xuICAgICAgcmVzdWx0W2tleV0gPSBbcHJldmlvdXNWYWx1ZSwgdG9WYWx1ZSh2YWx1ZSldXG4gICAgfVxuICB9XG5cbiAgcmV0dXJuIHJlc3VsdFxufVxuIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUF3QkEsU0FBZ0IsT0FDZCxLQUNBLFlBQW9DLFFBQzVCO0NBQ1IsTUFBTSxTQUFTLElBQUksZ0JBQWdCO0NBRW5DLEtBQUssTUFBTSxPQUFPLEtBQUs7RUFDckIsTUFBTSxNQUFNLElBQUk7RUFDaEIsSUFBSSxRQUFRLEtBQUEsR0FDVixPQUFPLElBQUksS0FBSyxVQUFVLEdBQUcsQ0FBQztDQUVsQztDQUVBLE9BQU8sT0FBTyxTQUFTO0FBQ3pCOzs7Ozs7Ozs7QUFVQSxTQUFTLFFBQVEsS0FBYztDQUM3QixJQUFJLENBQUMsS0FBSyxPQUFPO0NBRWpCLElBQUksUUFBUSxTQUFTLE9BQU87Q0FDNUIsSUFBSSxRQUFRLFFBQVEsT0FBTztDQUMzQixPQUFPLENBQUMsTUFBTSxNQUFNLEtBQUssQ0FBQyxNQUFNLE9BQU8sTUFBTSxDQUFDLE1BQU07QUFDdEQ7Ozs7Ozs7OztBQVNBLFNBQWdCLE9BQU8sS0FBZTtDQUNwQyxNQUFNLGVBQWUsSUFBSSxnQkFBZ0IsR0FBRztDQUU1QyxNQUFNLFNBQWtDLE9BQU8sT0FBTyxJQUFJO0NBRTFELEtBQUssTUFBTSxDQUFDLEtBQUssVUFBVSxhQUFhLFFBQVEsR0FBRztFQUNqRCxNQUFNLGdCQUFnQixPQUFPO0VBQzdCLElBQUksaUJBQWlCLE1BQ25CLE9BQU8sT0FBTyxRQUFRLEtBQUs7T0FDdEIsSUFBSSxNQUFNLFFBQVEsYUFBYSxHQUNwQyxjQUFjLEtBQUssUUFBUSxLQUFLLENBQUM7T0FFakMsT0FBTyxPQUFPLENBQUMsZUFBZSxRQUFRLEtBQUssQ0FBQztDQUVoRDtDQUVBLE9BQU87QUFDVCIsInhfZ29vZ2xlX2lnbm9yZUxpc3QiOlswXX0=