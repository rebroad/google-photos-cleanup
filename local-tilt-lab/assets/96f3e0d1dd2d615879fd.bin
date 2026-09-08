//#region node_modules/tailwind-merge/dist/bundle-mjs.mjs
/**
* Concatenates two arrays faster than the array spread operator.
*/
var concatArrays = (array1, array2) => {
	const combinedArray = new Array(array1.length + array2.length);
	for (let i = 0; i < array1.length; i++) combinedArray[i] = array1[i];
	for (let i = 0; i < array2.length; i++) combinedArray[array1.length + i] = array2[i];
	return combinedArray;
};
var createClassValidatorObject = (classGroupId, validator) => ({
	classGroupId,
	validator
});
var createClassPartObject = (nextPart = /* @__PURE__ */ new Map(), validators = null, classGroupId) => ({
	nextPart,
	validators,
	classGroupId
});
var CLASS_PART_SEPARATOR = "-";
var EMPTY_CONFLICTS = [];
var ARBITRARY_PROPERTY_PREFIX = "arbitrary..";
var createClassGroupUtils = (config) => {
	const classMap = createClassMap(config);
	const { conflictingClassGroups, conflictingClassGroupModifiers } = config;
	const getClassGroupId = (className) => {
		if (className.startsWith("[") && className.endsWith("]")) return getGroupIdForArbitraryProperty(className);
		const classParts = className.split(CLASS_PART_SEPARATOR);
		return getGroupRecursive(classParts, classParts[0] === "" && classParts.length > 1 ? 1 : 0, classMap);
	};
	const getConflictingClassGroupIds = (classGroupId, hasPostfixModifier) => {
		if (hasPostfixModifier) {
			const modifierConflicts = conflictingClassGroupModifiers[classGroupId];
			const baseConflicts = conflictingClassGroups[classGroupId];
			if (modifierConflicts) {
				if (baseConflicts) return concatArrays(baseConflicts, modifierConflicts);
				return modifierConflicts;
			}
			return baseConflicts || EMPTY_CONFLICTS;
		}
		return conflictingClassGroups[classGroupId] || EMPTY_CONFLICTS;
	};
	return {
		getClassGroupId,
		getConflictingClassGroupIds
	};
};
var getGroupRecursive = (classParts, startIndex, classPartObject) => {
	if (classParts.length - startIndex === 0) return classPartObject.classGroupId;
	const currentClassPart = classParts[startIndex];
	const nextClassPartObject = classPartObject.nextPart.get(currentClassPart);
	if (nextClassPartObject) {
		const result = getGroupRecursive(classParts, startIndex + 1, nextClassPartObject);
		if (result) return result;
	}
	const validators = classPartObject.validators;
	if (validators === null) return;
	const classRest = startIndex === 0 ? classParts.join(CLASS_PART_SEPARATOR) : classParts.slice(startIndex).join(CLASS_PART_SEPARATOR);
	const validatorsLength = validators.length;
	for (let i = 0; i < validatorsLength; i++) {
		const validatorObj = validators[i];
		if (validatorObj.validator(classRest)) return validatorObj.classGroupId;
	}
};
/**
* Get the class group ID for an arbitrary property.
*
* @param className - The class name to get the group ID for. Is expected to be string starting with `[` and ending with `]`.
*/
var getGroupIdForArbitraryProperty = (className) => className.slice(1, -1).indexOf(":") === -1 ? void 0 : (() => {
	const content = className.slice(1, -1);
	const colonIndex = content.indexOf(":");
	const property = content.slice(0, colonIndex);
	return property ? ARBITRARY_PROPERTY_PREFIX + property : void 0;
})();
/**
* Exported for testing only
*/
var createClassMap = (config) => {
	const { theme, classGroups } = config;
	return processClassGroups(classGroups, theme);
};
var processClassGroups = (classGroups, theme) => {
	const classMap = createClassPartObject();
	for (const classGroupId in classGroups) {
		const group = classGroups[classGroupId];
		processClassesRecursively(group, classMap, classGroupId, theme);
	}
	return classMap;
};
var processClassesRecursively = (classGroup, classPartObject, classGroupId, theme) => {
	const len = classGroup.length;
	for (let i = 0; i < len; i++) {
		const classDefinition = classGroup[i];
		processClassDefinition(classDefinition, classPartObject, classGroupId, theme);
	}
};
var processClassDefinition = (classDefinition, classPartObject, classGroupId, theme) => {
	if (typeof classDefinition === "string") {
		processStringDefinition(classDefinition, classPartObject, classGroupId);
		return;
	}
	if (typeof classDefinition === "function") {
		processFunctionDefinition(classDefinition, classPartObject, classGroupId, theme);
		return;
	}
	processObjectDefinition(classDefinition, classPartObject, classGroupId, theme);
};
var processStringDefinition = (classDefinition, classPartObject, classGroupId) => {
	const classPartObjectToEdit = classDefinition === "" ? classPartObject : getPart(classPartObject, classDefinition);
	classPartObjectToEdit.classGroupId = classGroupId;
};
var processFunctionDefinition = (classDefinition, classPartObject, classGroupId, theme) => {
	if (isThemeGetter(classDefinition)) {
		processClassesRecursively(classDefinition(theme), classPartObject, classGroupId, theme);
		return;
	}
	if (classPartObject.validators === null) classPartObject.validators = [];
	classPartObject.validators.push(createClassValidatorObject(classGroupId, classDefinition));
};
var processObjectDefinition = (classDefinition, classPartObject, classGroupId, theme) => {
	const entries = Object.entries(classDefinition);
	const len = entries.length;
	for (let i = 0; i < len; i++) {
		const [key, value] = entries[i];
		processClassesRecursively(value, getPart(classPartObject, key), classGroupId, theme);
	}
};
var getPart = (classPartObject, path) => {
	let current = classPartObject;
	const parts = path.split(CLASS_PART_SEPARATOR);
	const len = parts.length;
	for (let i = 0; i < len; i++) {
		const part = parts[i];
		let next = current.nextPart.get(part);
		if (!next) {
			next = createClassPartObject();
			current.nextPart.set(part, next);
		}
		current = next;
	}
	return current;
};
var isThemeGetter = (func) => "isThemeGetter" in func && func.isThemeGetter === true;
var createLruCache = (maxCacheSize) => {
	if (maxCacheSize < 1) return {
		get: () => void 0,
		set: () => {}
	};
	let cacheSize = 0;
	let cache = Object.create(null);
	let previousCache = Object.create(null);
	const update = (key, value) => {
		cache[key] = value;
		cacheSize++;
		if (cacheSize > maxCacheSize) {
			cacheSize = 0;
			previousCache = cache;
			cache = Object.create(null);
		}
	};
	return {
		get(key) {
			let value = cache[key];
			if (value !== void 0) return value;
			if ((value = previousCache[key]) !== void 0) {
				update(key, value);
				return value;
			}
		},
		set(key, value) {
			if (key in cache) cache[key] = value;
			else update(key, value);
		}
	};
};
var IMPORTANT_MODIFIER = "!";
var MODIFIER_SEPARATOR = ":";
var EMPTY_MODIFIERS = [];
var createResultObject = (modifiers, hasImportantModifier, baseClassName, maybePostfixModifierPosition, isExternal) => ({
	modifiers,
	hasImportantModifier,
	baseClassName,
	maybePostfixModifierPosition,
	isExternal
});
var createParseClassName = (config) => {
	const { prefix, experimentalParseClassName } = config;
	/**
	* Parse class name into parts.
	*
	* Inspired by `splitAtTopLevelOnly` used in Tailwind CSS
	* @see https://github.com/tailwindlabs/tailwindcss/blob/v3.2.2/src/util/splitAtTopLevelOnly.js
	*/
	let parseClassName = (className) => {
		const modifiers = [];
		let bracketDepth = 0;
		let parenDepth = 0;
		let modifierStart = 0;
		let postfixModifierPosition;
		const len = className.length;
		for (let index = 0; index < len; index++) {
			const currentCharacter = className[index];
			if (bracketDepth === 0 && parenDepth === 0) {
				if (currentCharacter === MODIFIER_SEPARATOR) {
					modifiers.push(className.slice(modifierStart, index));
					modifierStart = index + 1;
					continue;
				}
				if (currentCharacter === "/") {
					postfixModifierPosition = index;
					continue;
				}
			}
			if (currentCharacter === "[") bracketDepth++;
			else if (currentCharacter === "]") bracketDepth--;
			else if (currentCharacter === "(") parenDepth++;
			else if (currentCharacter === ")") parenDepth--;
		}
		const baseClassNameWithImportantModifier = modifiers.length === 0 ? className : className.slice(modifierStart);
		let baseClassName = baseClassNameWithImportantModifier;
		let hasImportantModifier = false;
		if (baseClassNameWithImportantModifier.endsWith(IMPORTANT_MODIFIER)) {
			baseClassName = baseClassNameWithImportantModifier.slice(0, -1);
			hasImportantModifier = true;
		} else if (baseClassNameWithImportantModifier.startsWith(IMPORTANT_MODIFIER)) {
			baseClassName = baseClassNameWithImportantModifier.slice(1);
			hasImportantModifier = true;
		}
		const maybePostfixModifierPosition = postfixModifierPosition && postfixModifierPosition > modifierStart ? postfixModifierPosition - modifierStart : void 0;
		return createResultObject(modifiers, hasImportantModifier, baseClassName, maybePostfixModifierPosition);
	};
	if (prefix) {
		const fullPrefix = prefix + MODIFIER_SEPARATOR;
		const parseClassNameOriginal = parseClassName;
		parseClassName = (className) => className.startsWith(fullPrefix) ? parseClassNameOriginal(className.slice(fullPrefix.length)) : createResultObject(EMPTY_MODIFIERS, false, className, void 0, true);
	}
	if (experimentalParseClassName) {
		const parseClassNameOriginal = parseClassName;
		parseClassName = (className) => experimentalParseClassName({
			className,
			parseClassName: parseClassNameOriginal
		});
	}
	return parseClassName;
};
/**
* Sorts modifiers according to following schema:
* - Predefined modifiers are sorted alphabetically
* - When an arbitrary variant appears, it must be preserved which modifiers are before and after it
*/
var createSortModifiers = (config) => {
	const modifierWeights = /* @__PURE__ */ new Map();
	config.orderSensitiveModifiers.forEach((mod, index) => {
		modifierWeights.set(mod, 1e6 + index);
	});
	return (modifiers) => {
		const result = [];
		let currentSegment = [];
		for (let i = 0; i < modifiers.length; i++) {
			const modifier = modifiers[i];
			const isArbitrary = modifier[0] === "[";
			const isOrderSensitive = modifierWeights.has(modifier);
			if (isArbitrary || isOrderSensitive) {
				if (currentSegment.length > 0) {
					currentSegment.sort();
					result.push(...currentSegment);
					currentSegment = [];
				}
				result.push(modifier);
			} else currentSegment.push(modifier);
		}
		if (currentSegment.length > 0) {
			currentSegment.sort();
			result.push(...currentSegment);
		}
		return result;
	};
};
var createConfigUtils = (config) => ({
	cache: createLruCache(config.cacheSize),
	parseClassName: createParseClassName(config),
	sortModifiers: createSortModifiers(config),
	postfixLookupClassGroupIds: createPostfixLookupClassGroupIds(config),
	...createClassGroupUtils(config)
});
var createPostfixLookupClassGroupIds = (config) => {
	const lookup = Object.create(null);
	const classGroupIds = config.postfixLookupClassGroups;
	if (classGroupIds) for (let i = 0; i < classGroupIds.length; i++) lookup[classGroupIds[i]] = true;
	return lookup;
};
var SPLIT_CLASSES_REGEX = /\s+/;
var mergeClassList = (classList, configUtils) => {
	const { parseClassName, getClassGroupId, getConflictingClassGroupIds, sortModifiers, postfixLookupClassGroupIds } = configUtils;
	/**
	* Set of classGroupIds in following format:
	* `{importantModifier}{variantModifiers}{classGroupId}`
	* @example 'float'
	* @example 'hover:focus:bg-color'
	* @example 'md:!pr'
	*/
	const classGroupsInConflict = [];
	const classNames = classList.trim().split(SPLIT_CLASSES_REGEX);
	let result = "";
	for (let index = classNames.length - 1; index >= 0; index -= 1) {
		const originalClassName = classNames[index];
		const { isExternal, modifiers, hasImportantModifier, baseClassName, maybePostfixModifierPosition } = parseClassName(originalClassName);
		if (isExternal) {
			result = originalClassName + (result.length > 0 ? " " + result : result);
			continue;
		}
		let hasPostfixModifier = !!maybePostfixModifierPosition;
		let classGroupId;
		if (hasPostfixModifier) {
			classGroupId = getClassGroupId(baseClassName.substring(0, maybePostfixModifierPosition));
			const classGroupIdWithPostfix = classGroupId && postfixLookupClassGroupIds[classGroupId] ? getClassGroupId(baseClassName) : void 0;
			if (classGroupIdWithPostfix && classGroupIdWithPostfix !== classGroupId) {
				classGroupId = classGroupIdWithPostfix;
				hasPostfixModifier = false;
			}
		} else classGroupId = getClassGroupId(baseClassName);
		if (!classGroupId) {
			if (!hasPostfixModifier) {
				result = originalClassName + (result.length > 0 ? " " + result : result);
				continue;
			}
			classGroupId = getClassGroupId(baseClassName);
			if (!classGroupId) {
				result = originalClassName + (result.length > 0 ? " " + result : result);
				continue;
			}
			hasPostfixModifier = false;
		}
		const variantModifier = modifiers.length === 0 ? "" : modifiers.length === 1 ? modifiers[0] : sortModifiers(modifiers).join(":");
		const modifierId = hasImportantModifier ? variantModifier + IMPORTANT_MODIFIER : variantModifier;
		const classId = modifierId + classGroupId;
		if (classGroupsInConflict.indexOf(classId) > -1) continue;
		classGroupsInConflict.push(classId);
		const conflictGroups = getConflictingClassGroupIds(classGroupId, hasPostfixModifier);
		for (let i = 0; i < conflictGroups.length; ++i) {
			const group = conflictGroups[i];
			classGroupsInConflict.push(modifierId + group);
		}
		result = originalClassName + (result.length > 0 ? " " + result : result);
	}
	return result;
};
/**
* The code in this file is copied from https://github.com/lukeed/clsx and modified to suit the needs of tailwind-merge better.
*
* Specifically:
* - Runtime code from https://github.com/lukeed/clsx/blob/v1.2.1/src/index.js
* - TypeScript types from https://github.com/lukeed/clsx/blob/v1.2.1/clsx.d.ts
*
* Original code has MIT license: Copyright (c) Luke Edwards <luke.edwards05@gmail.com> (lukeed.com)
*/
var twJoin = (...classLists) => {
	let index = 0;
	let argument;
	let resolvedValue;
	let string = "";
	while (index < classLists.length) if (argument = classLists[index++]) {
		if (resolvedValue = toValue(argument)) {
			string && (string += " ");
			string += resolvedValue;
		}
	}
	return string;
};
var toValue = (mix) => {
	if (typeof mix === "string") return mix;
	let resolvedValue;
	let string = "";
	for (let k = 0; k < mix.length; k++) if (mix[k]) {
		if (resolvedValue = toValue(mix[k])) {
			string && (string += " ");
			string += resolvedValue;
		}
	}
	return string;
};
var createTailwindMerge = (createConfigFirst, ...createConfigRest) => {
	let configUtils;
	let cacheGet;
	let cacheSet;
	let functionToCall;
	const initTailwindMerge = (classList) => {
		configUtils = createConfigUtils(createConfigRest.reduce((previousConfig, createConfigCurrent) => createConfigCurrent(previousConfig), createConfigFirst()));
		cacheGet = configUtils.cache.get;
		cacheSet = configUtils.cache.set;
		functionToCall = tailwindMerge;
		return tailwindMerge(classList);
	};
	const tailwindMerge = (classList) => {
		const cachedResult = cacheGet(classList);
		if (cachedResult) return cachedResult;
		const result = mergeClassList(classList, configUtils);
		cacheSet(classList, result);
		return result;
	};
	functionToCall = initTailwindMerge;
	return (...args) => functionToCall(twJoin(...args));
};
var fallbackThemeArr = [];
var fromTheme = (key) => {
	const themeGetter = (theme) => theme[key] || fallbackThemeArr;
	themeGetter.isThemeGetter = true;
	return themeGetter;
};
var arbitraryValueRegex = /^\[(?:(\w[\w-]*):)?(.+)\]$/i;
var arbitraryVariableRegex = /^\((?:(\w[\w-]*):)?(.+)\)$/i;
var fractionRegex = /^\d+(?:\.\d+)?\/\d+(?:\.\d+)?$/;
var tshirtUnitRegex = /^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$/;
var lengthUnitRegex = /\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$/;
var colorFunctionRegex = /^(rgba?|hsla?|hwb|(ok)?(lab|lch)|color-mix)\(.+\)$/;
var shadowRegex = /^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)/;
var imageRegex = /^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$/;
var isFraction = (value) => fractionRegex.test(value);
var isNumber = (value) => !!value && !Number.isNaN(Number(value));
var isInteger = (value) => !!value && Number.isInteger(Number(value));
var isPercent = (value) => value.endsWith("%") && isNumber(value.slice(0, -1));
var isTshirtSize = (value) => tshirtUnitRegex.test(value);
var isAny = () => true;
var isLengthOnly = (value) => lengthUnitRegex.test(value) && !colorFunctionRegex.test(value);
var isNever = () => false;
var isShadow = (value) => shadowRegex.test(value);
var isImage = (value) => imageRegex.test(value);
var isAnyNonArbitrary = (value) => !isArbitraryValue(value) && !isArbitraryVariable(value);
var isNamedContainerQuery = (value) => value.startsWith("@container") && (value[10] === "/" && value[11] !== void 0 || value[11] === "s" && value[16] !== void 0 && value.startsWith("-size/", 10) || value[11] === "n" && value[18] !== void 0 && value.startsWith("-normal/", 10));
var isArbitrarySize = (value) => getIsArbitraryValue(value, isLabelSize, isNever);
var isArbitraryValue = (value) => arbitraryValueRegex.test(value);
var isArbitraryLength = (value) => getIsArbitraryValue(value, isLabelLength, isLengthOnly);
var isArbitraryNumber = (value) => getIsArbitraryValue(value, isLabelNumber, isNumber);
var isArbitraryWeight = (value) => getIsArbitraryValue(value, isLabelWeight, isAny);
var isArbitraryFamilyName = (value) => getIsArbitraryValue(value, isLabelFamilyName, isNever);
var isArbitraryPosition = (value) => getIsArbitraryValue(value, isLabelPosition, isNever);
var isArbitraryImage = (value) => getIsArbitraryValue(value, isLabelImage, isImage);
var isArbitraryShadow = (value) => getIsArbitraryValue(value, isLabelShadow, isShadow);
var isArbitraryVariable = (value) => arbitraryVariableRegex.test(value);
var isArbitraryVariableLength = (value) => getIsArbitraryVariable(value, isLabelLength);
var isArbitraryVariableFamilyName = (value) => getIsArbitraryVariable(value, isLabelFamilyName);
var isArbitraryVariablePosition = (value) => getIsArbitraryVariable(value, isLabelPosition);
var isArbitraryVariableSize = (value) => getIsArbitraryVariable(value, isLabelSize);
var isArbitraryVariableImage = (value) => getIsArbitraryVariable(value, isLabelImage);
var isArbitraryVariableShadow = (value) => getIsArbitraryVariable(value, isLabelShadow, true);
var isArbitraryVariableWeight = (value) => getIsArbitraryVariable(value, isLabelWeight, true);
var getIsArbitraryValue = (value, testLabel, testValue) => {
	const result = arbitraryValueRegex.exec(value);
	if (result) {
		if (result[1]) return testLabel(result[1]);
		return testValue(result[2]);
	}
	return false;
};
var getIsArbitraryVariable = (value, testLabel, shouldMatchNoLabel = false) => {
	const result = arbitraryVariableRegex.exec(value);
	if (result) {
		if (result[1]) return testLabel(result[1]);
		return shouldMatchNoLabel;
	}
	return false;
};
var isLabelPosition = (label) => label === "position" || label === "percentage";
var isLabelImage = (label) => label === "image" || label === "url";
var isLabelSize = (label) => label === "length" || label === "size" || label === "bg-size";
var isLabelLength = (label) => label === "length";
var isLabelNumber = (label) => label === "number";
var isLabelFamilyName = (label) => label === "family-name";
var isLabelWeight = (label) => label === "number" || label === "weight";
var isLabelShadow = (label) => label === "shadow";
var validators = /*#__PURE__*/ Object.defineProperty({
	__proto__: null,
	isAny,
	isAnyNonArbitrary,
	isArbitraryFamilyName,
	isArbitraryImage,
	isArbitraryLength,
	isArbitraryNumber,
	isArbitraryPosition,
	isArbitraryShadow,
	isArbitrarySize,
	isArbitraryValue,
	isArbitraryVariable,
	isArbitraryVariableFamilyName,
	isArbitraryVariableImage,
	isArbitraryVariableLength,
	isArbitraryVariablePosition,
	isArbitraryVariableShadow,
	isArbitraryVariableSize,
	isArbitraryVariableWeight,
	isArbitraryWeight,
	isFraction,
	isInteger,
	isNamedContainerQuery,
	isNumber,
	isPercent,
	isTshirtSize
}, Symbol.toStringTag, { value: "Module" });
var getDefaultConfig = () => {
	/**
	* Theme getters for theme variable namespaces
	* @see https://tailwindcss.com/docs/theme#theme-variable-namespaces
	*/
	const themeColor = fromTheme("color");
	const themeFont = fromTheme("font");
	const themeText = fromTheme("text");
	const themeFontWeight = fromTheme("font-weight");
	const themeTracking = fromTheme("tracking");
	const themeLeading = fromTheme("leading");
	const themeBreakpoint = fromTheme("breakpoint");
	const themeContainer = fromTheme("container");
	const themeSpacing = fromTheme("spacing");
	const themeRadius = fromTheme("radius");
	const themeShadow = fromTheme("shadow");
	const themeInsetShadow = fromTheme("inset-shadow");
	const themeTextShadow = fromTheme("text-shadow");
	const themeDropShadow = fromTheme("drop-shadow");
	const themeBlur = fromTheme("blur");
	const themePerspective = fromTheme("perspective");
	const themeAspect = fromTheme("aspect");
	const themeEase = fromTheme("ease");
	const themeAnimate = fromTheme("animate");
	/**
	* Helpers to avoid repeating the same scales
	*
	* We use functions that create a new array every time they're called instead of static arrays.
	* This ensures that users who modify any scale by mutating the array (e.g. with `array.push(element)`) don't accidentally mutate arrays in other parts of the config.
	*/
	const scaleBreak = () => [
		"auto",
		"avoid",
		"all",
		"avoid-page",
		"page",
		"left",
		"right",
		"column"
	];
	const scalePosition = () => [
		"center",
		"top",
		"bottom",
		"left",
		"right",
		"top-left",
		"left-top",
		"top-right",
		"right-top",
		"bottom-right",
		"right-bottom",
		"bottom-left",
		"left-bottom"
	];
	const scalePositionWithArbitrary = () => [
		...scalePosition(),
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleOverflow = () => [
		"auto",
		"hidden",
		"clip",
		"visible",
		"scroll"
	];
	const scaleOverscroll = () => [
		"auto",
		"contain",
		"none"
	];
	const scaleUnambiguousSpacing = () => [
		isArbitraryVariable,
		isArbitraryValue,
		themeSpacing
	];
	const scaleInset = () => [
		isFraction,
		"full",
		"auto",
		...scaleUnambiguousSpacing()
	];
	const scaleGridTemplateColsRows = () => [
		isInteger,
		"none",
		"subgrid",
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleGridColRowStartAndEnd = () => [
		"auto",
		{ span: [
			"full",
			isInteger,
			isArbitraryVariable,
			isArbitraryValue
		] },
		isInteger,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleGridColRowStartOrEnd = () => [
		isInteger,
		"auto",
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleGridAutoColsRows = () => [
		"auto",
		"min",
		"max",
		"fr",
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleAlignPrimaryAxis = () => [
		"start",
		"end",
		"center",
		"between",
		"around",
		"evenly",
		"stretch",
		"baseline",
		"center-safe",
		"end-safe"
	];
	const scaleAlignSecondaryAxis = () => [
		"start",
		"end",
		"center",
		"stretch",
		"center-safe",
		"end-safe"
	];
	const scaleMargin = () => ["auto", ...scaleUnambiguousSpacing()];
	const scaleSizing = () => [
		isFraction,
		"auto",
		"full",
		"dvw",
		"dvh",
		"lvw",
		"lvh",
		"svw",
		"svh",
		"min",
		"max",
		"fit",
		...scaleUnambiguousSpacing()
	];
	const scaleSizingInline = () => [
		isFraction,
		"screen",
		"full",
		"dvw",
		"lvw",
		"svw",
		"min",
		"max",
		"fit",
		...scaleUnambiguousSpacing()
	];
	const scaleSizingBlock = () => [
		isFraction,
		"screen",
		"full",
		"lh",
		"dvh",
		"lvh",
		"svh",
		"min",
		"max",
		"fit",
		...scaleUnambiguousSpacing()
	];
	const scaleColor = () => [
		themeColor,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleBgPosition = () => [
		...scalePosition(),
		isArbitraryVariablePosition,
		isArbitraryPosition,
		{ position: [isArbitraryVariable, isArbitraryValue] }
	];
	const scaleBgRepeat = () => ["no-repeat", { repeat: [
		"",
		"x",
		"y",
		"space",
		"round"
	] }];
	const scaleBgSize = () => [
		"auto",
		"cover",
		"contain",
		isArbitraryVariableSize,
		isArbitrarySize,
		{ size: [isArbitraryVariable, isArbitraryValue] }
	];
	const scaleGradientStopPosition = () => [
		isPercent,
		isArbitraryVariableLength,
		isArbitraryLength
	];
	const scaleRadius = () => [
		"",
		"none",
		"full",
		themeRadius,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleBorderWidth = () => [
		"",
		isNumber,
		isArbitraryVariableLength,
		isArbitraryLength
	];
	const scaleLineStyle = () => [
		"solid",
		"dashed",
		"dotted",
		"double"
	];
	const scaleBlendMode = () => [
		"normal",
		"multiply",
		"screen",
		"overlay",
		"darken",
		"lighten",
		"color-dodge",
		"color-burn",
		"hard-light",
		"soft-light",
		"difference",
		"exclusion",
		"hue",
		"saturation",
		"color",
		"luminosity"
	];
	const scaleMaskImagePosition = () => [
		isNumber,
		isPercent,
		isArbitraryVariablePosition,
		isArbitraryPosition
	];
	const scaleBlur = () => [
		"",
		"none",
		themeBlur,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleRotate = () => [
		"none",
		isNumber,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleScale = () => [
		"none",
		isNumber,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleSkew = () => [
		isNumber,
		isArbitraryVariable,
		isArbitraryValue
	];
	const scaleTranslate = () => [
		isFraction,
		"full",
		...scaleUnambiguousSpacing()
	];
	return {
		cacheSize: 500,
		theme: {
			animate: [
				"spin",
				"ping",
				"pulse",
				"bounce"
			],
			aspect: ["video"],
			blur: [isTshirtSize],
			breakpoint: [isTshirtSize],
			color: [isAny],
			container: [isTshirtSize],
			"drop-shadow": [isTshirtSize],
			ease: [
				"in",
				"out",
				"in-out"
			],
			font: [isAnyNonArbitrary],
			"font-weight": [
				"thin",
				"extralight",
				"light",
				"normal",
				"medium",
				"semibold",
				"bold",
				"extrabold",
				"black"
			],
			"inset-shadow": [isTshirtSize],
			leading: [
				"none",
				"tight",
				"snug",
				"normal",
				"relaxed",
				"loose"
			],
			perspective: [
				"dramatic",
				"near",
				"normal",
				"midrange",
				"distant",
				"none"
			],
			radius: [isTshirtSize],
			shadow: [isTshirtSize],
			spacing: ["px", isNumber],
			text: [isTshirtSize],
			"text-shadow": [isTshirtSize],
			tracking: [
				"tighter",
				"tight",
				"normal",
				"wide",
				"wider",
				"widest"
			]
		},
		classGroups: {
			/**
			* Aspect Ratio
			* @see https://tailwindcss.com/docs/aspect-ratio
			*/
			aspect: [{ aspect: [
				"auto",
				"square",
				isFraction,
				isArbitraryValue,
				isArbitraryVariable,
				themeAspect
			] }],
			/**
			* Container
			* @see https://tailwindcss.com/docs/container
			* @deprecated since Tailwind CSS v4.0.0
			*/
			container: ["container"],
			/**
			* Container Type
			* @see https://tailwindcss.com/docs/responsive-design#container-queries
			*/
			"container-type": [{ "@container": [
				"",
				"normal",
				"size",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Container Name
			* @see https://tailwindcss.com/docs/responsive-design#named-containers
			*/
			"container-named": [isNamedContainerQuery],
			/**
			* Columns
			* @see https://tailwindcss.com/docs/columns
			*/
			columns: [{ columns: [
				isNumber,
				isArbitraryValue,
				isArbitraryVariable,
				themeContainer
			] }],
			/**
			* Break After
			* @see https://tailwindcss.com/docs/break-after
			*/
			"break-after": [{ "break-after": scaleBreak() }],
			/**
			* Break Before
			* @see https://tailwindcss.com/docs/break-before
			*/
			"break-before": [{ "break-before": scaleBreak() }],
			/**
			* Break Inside
			* @see https://tailwindcss.com/docs/break-inside
			*/
			"break-inside": [{ "break-inside": [
				"auto",
				"avoid",
				"avoid-page",
				"avoid-column"
			] }],
			/**
			* Box Decoration Break
			* @see https://tailwindcss.com/docs/box-decoration-break
			*/
			"box-decoration": [{ "box-decoration": ["slice", "clone"] }],
			/**
			* Box Sizing
			* @see https://tailwindcss.com/docs/box-sizing
			*/
			box: [{ box: ["border", "content"] }],
			/**
			* Display
			* @see https://tailwindcss.com/docs/display
			*/
			display: [
				"block",
				"inline-block",
				"inline",
				"flex",
				"inline-flex",
				"table",
				"inline-table",
				"table-caption",
				"table-cell",
				"table-column",
				"table-column-group",
				"table-footer-group",
				"table-header-group",
				"table-row-group",
				"table-row",
				"flow-root",
				"grid",
				"inline-grid",
				"contents",
				"list-item",
				"hidden"
			],
			/**
			* Screen Reader Only
			* @see https://tailwindcss.com/docs/display#screen-reader-only
			*/
			sr: ["sr-only", "not-sr-only"],
			/**
			* Floats
			* @see https://tailwindcss.com/docs/float
			*/
			float: [{ float: [
				"right",
				"left",
				"none",
				"start",
				"end"
			] }],
			/**
			* Clear
			* @see https://tailwindcss.com/docs/clear
			*/
			clear: [{ clear: [
				"left",
				"right",
				"both",
				"none",
				"start",
				"end"
			] }],
			/**
			* Isolation
			* @see https://tailwindcss.com/docs/isolation
			*/
			isolation: ["isolate", "isolation-auto"],
			/**
			* Object Fit
			* @see https://tailwindcss.com/docs/object-fit
			*/
			"object-fit": [{ object: [
				"contain",
				"cover",
				"fill",
				"none",
				"scale-down"
			] }],
			/**
			* Object Position
			* @see https://tailwindcss.com/docs/object-position
			*/
			"object-position": [{ object: scalePositionWithArbitrary() }],
			/**
			* Overflow
			* @see https://tailwindcss.com/docs/overflow
			*/
			overflow: [{ overflow: scaleOverflow() }],
			/**
			* Overflow X
			* @see https://tailwindcss.com/docs/overflow
			*/
			"overflow-x": [{ "overflow-x": scaleOverflow() }],
			/**
			* Overflow Y
			* @see https://tailwindcss.com/docs/overflow
			*/
			"overflow-y": [{ "overflow-y": scaleOverflow() }],
			/**
			* Overscroll Behavior
			* @see https://tailwindcss.com/docs/overscroll-behavior
			*/
			overscroll: [{ overscroll: scaleOverscroll() }],
			/**
			* Overscroll Behavior X
			* @see https://tailwindcss.com/docs/overscroll-behavior
			*/
			"overscroll-x": [{ "overscroll-x": scaleOverscroll() }],
			/**
			* Overscroll Behavior Y
			* @see https://tailwindcss.com/docs/overscroll-behavior
			*/
			"overscroll-y": [{ "overscroll-y": scaleOverscroll() }],
			/**
			* Position
			* @see https://tailwindcss.com/docs/position
			*/
			position: [
				"static",
				"fixed",
				"absolute",
				"relative",
				"sticky"
			],
			/**
			* Inset
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			inset: [{ inset: scaleInset() }],
			/**
			* Inset Inline
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			"inset-x": [{ "inset-x": scaleInset() }],
			/**
			* Inset Block
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			"inset-y": [{ "inset-y": scaleInset() }],
			/**
			* Inset Inline Start
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			* @todo class group will be renamed to `inset-s` in next major release
			*/
			start: [{
				"inset-s": scaleInset(),
				/**
				* @deprecated since Tailwind CSS v4.2.0 in favor of `inset-s-*` utilities.
				* @see https://github.com/tailwindlabs/tailwindcss/pull/19613
				*/
				start: scaleInset()
			}],
			/**
			* Inset Inline End
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			* @todo class group will be renamed to `inset-e` in next major release
			*/
			end: [{
				"inset-e": scaleInset(),
				/**
				* @deprecated since Tailwind CSS v4.2.0 in favor of `inset-e-*` utilities.
				* @see https://github.com/tailwindlabs/tailwindcss/pull/19613
				*/
				end: scaleInset()
			}],
			/**
			* Inset Block Start
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			"inset-bs": [{ "inset-bs": scaleInset() }],
			/**
			* Inset Block End
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			"inset-be": [{ "inset-be": scaleInset() }],
			/**
			* Top
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			top: [{ top: scaleInset() }],
			/**
			* Right
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			right: [{ right: scaleInset() }],
			/**
			* Bottom
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			bottom: [{ bottom: scaleInset() }],
			/**
			* Left
			* @see https://tailwindcss.com/docs/top-right-bottom-left
			*/
			left: [{ left: scaleInset() }],
			/**
			* Visibility
			* @see https://tailwindcss.com/docs/visibility
			*/
			visibility: [
				"visible",
				"invisible",
				"collapse"
			],
			/**
			* Z-Index
			* @see https://tailwindcss.com/docs/z-index
			*/
			z: [{ z: [
				isInteger,
				"auto",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Flex Basis
			* @see https://tailwindcss.com/docs/flex-basis
			*/
			basis: [{ basis: [
				isFraction,
				"full",
				"auto",
				themeContainer,
				...scaleUnambiguousSpacing()
			] }],
			/**
			* Flex Direction
			* @see https://tailwindcss.com/docs/flex-direction
			*/
			"flex-direction": [{ flex: [
				"row",
				"row-reverse",
				"col",
				"col-reverse"
			] }],
			/**
			* Flex Wrap
			* @see https://tailwindcss.com/docs/flex-wrap
			*/
			"flex-wrap": [{ flex: [
				"nowrap",
				"wrap",
				"wrap-reverse"
			] }],
			/**
			* Flex
			* @see https://tailwindcss.com/docs/flex
			*/
			flex: [{ flex: [
				isNumber,
				isFraction,
				"auto",
				"initial",
				"none",
				isArbitraryValue
			] }],
			/**
			* Flex Grow
			* @see https://tailwindcss.com/docs/flex-grow
			*/
			grow: [{ grow: [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Flex Shrink
			* @see https://tailwindcss.com/docs/flex-shrink
			*/
			shrink: [{ shrink: [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Order
			* @see https://tailwindcss.com/docs/order
			*/
			order: [{ order: [
				isInteger,
				"first",
				"last",
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Grid Template Columns
			* @see https://tailwindcss.com/docs/grid-template-columns
			*/
			"grid-cols": [{ "grid-cols": scaleGridTemplateColsRows() }],
			/**
			* Grid Column Start / End
			* @see https://tailwindcss.com/docs/grid-column
			*/
			"col-start-end": [{ col: scaleGridColRowStartAndEnd() }],
			/**
			* Grid Column Start
			* @see https://tailwindcss.com/docs/grid-column
			*/
			"col-start": [{ "col-start": scaleGridColRowStartOrEnd() }],
			/**
			* Grid Column End
			* @see https://tailwindcss.com/docs/grid-column
			*/
			"col-end": [{ "col-end": scaleGridColRowStartOrEnd() }],
			/**
			* Grid Template Rows
			* @see https://tailwindcss.com/docs/grid-template-rows
			*/
			"grid-rows": [{ "grid-rows": scaleGridTemplateColsRows() }],
			/**
			* Grid Row Start / End
			* @see https://tailwindcss.com/docs/grid-row
			*/
			"row-start-end": [{ row: scaleGridColRowStartAndEnd() }],
			/**
			* Grid Row Start
			* @see https://tailwindcss.com/docs/grid-row
			*/
			"row-start": [{ "row-start": scaleGridColRowStartOrEnd() }],
			/**
			* Grid Row End
			* @see https://tailwindcss.com/docs/grid-row
			*/
			"row-end": [{ "row-end": scaleGridColRowStartOrEnd() }],
			/**
			* Grid Auto Flow
			* @see https://tailwindcss.com/docs/grid-auto-flow
			*/
			"grid-flow": [{ "grid-flow": [
				"row",
				"col",
				"dense",
				"row-dense",
				"col-dense"
			] }],
			/**
			* Grid Auto Columns
			* @see https://tailwindcss.com/docs/grid-auto-columns
			*/
			"auto-cols": [{ "auto-cols": scaleGridAutoColsRows() }],
			/**
			* Grid Auto Rows
			* @see https://tailwindcss.com/docs/grid-auto-rows
			*/
			"auto-rows": [{ "auto-rows": scaleGridAutoColsRows() }],
			/**
			* Gap
			* @see https://tailwindcss.com/docs/gap
			*/
			gap: [{ gap: scaleUnambiguousSpacing() }],
			/**
			* Gap X
			* @see https://tailwindcss.com/docs/gap
			*/
			"gap-x": [{ "gap-x": scaleUnambiguousSpacing() }],
			/**
			* Gap Y
			* @see https://tailwindcss.com/docs/gap
			*/
			"gap-y": [{ "gap-y": scaleUnambiguousSpacing() }],
			/**
			* Justify Content
			* @see https://tailwindcss.com/docs/justify-content
			*/
			"justify-content": [{ justify: [...scaleAlignPrimaryAxis(), "normal"] }],
			/**
			* Justify Items
			* @see https://tailwindcss.com/docs/justify-items
			*/
			"justify-items": [{ "justify-items": [...scaleAlignSecondaryAxis(), "normal"] }],
			/**
			* Justify Self
			* @see https://tailwindcss.com/docs/justify-self
			*/
			"justify-self": [{ "justify-self": ["auto", ...scaleAlignSecondaryAxis()] }],
			/**
			* Align Content
			* @see https://tailwindcss.com/docs/align-content
			*/
			"align-content": [{ content: ["normal", ...scaleAlignPrimaryAxis()] }],
			/**
			* Align Items
			* @see https://tailwindcss.com/docs/align-items
			*/
			"align-items": [{ items: [...scaleAlignSecondaryAxis(), { baseline: ["", "last"] }] }],
			/**
			* Align Self
			* @see https://tailwindcss.com/docs/align-self
			*/
			"align-self": [{ self: [
				"auto",
				...scaleAlignSecondaryAxis(),
				{ baseline: ["", "last"] }
			] }],
			/**
			* Place Content
			* @see https://tailwindcss.com/docs/place-content
			*/
			"place-content": [{ "place-content": scaleAlignPrimaryAxis() }],
			/**
			* Place Items
			* @see https://tailwindcss.com/docs/place-items
			*/
			"place-items": [{ "place-items": [...scaleAlignSecondaryAxis(), "baseline"] }],
			/**
			* Place Self
			* @see https://tailwindcss.com/docs/place-self
			*/
			"place-self": [{ "place-self": ["auto", ...scaleAlignSecondaryAxis()] }],
			/**
			* Padding
			* @see https://tailwindcss.com/docs/padding
			*/
			p: [{ p: scaleUnambiguousSpacing() }],
			/**
			* Padding Inline
			* @see https://tailwindcss.com/docs/padding
			*/
			px: [{ px: scaleUnambiguousSpacing() }],
			/**
			* Padding Block
			* @see https://tailwindcss.com/docs/padding
			*/
			py: [{ py: scaleUnambiguousSpacing() }],
			/**
			* Padding Inline Start
			* @see https://tailwindcss.com/docs/padding
			*/
			ps: [{ ps: scaleUnambiguousSpacing() }],
			/**
			* Padding Inline End
			* @see https://tailwindcss.com/docs/padding
			*/
			pe: [{ pe: scaleUnambiguousSpacing() }],
			/**
			* Padding Block Start
			* @see https://tailwindcss.com/docs/padding
			*/
			pbs: [{ pbs: scaleUnambiguousSpacing() }],
			/**
			* Padding Block End
			* @see https://tailwindcss.com/docs/padding
			*/
			pbe: [{ pbe: scaleUnambiguousSpacing() }],
			/**
			* Padding Top
			* @see https://tailwindcss.com/docs/padding
			*/
			pt: [{ pt: scaleUnambiguousSpacing() }],
			/**
			* Padding Right
			* @see https://tailwindcss.com/docs/padding
			*/
			pr: [{ pr: scaleUnambiguousSpacing() }],
			/**
			* Padding Bottom
			* @see https://tailwindcss.com/docs/padding
			*/
			pb: [{ pb: scaleUnambiguousSpacing() }],
			/**
			* Padding Left
			* @see https://tailwindcss.com/docs/padding
			*/
			pl: [{ pl: scaleUnambiguousSpacing() }],
			/**
			* Margin
			* @see https://tailwindcss.com/docs/margin
			*/
			m: [{ m: scaleMargin() }],
			/**
			* Margin Inline
			* @see https://tailwindcss.com/docs/margin
			*/
			mx: [{ mx: scaleMargin() }],
			/**
			* Margin Block
			* @see https://tailwindcss.com/docs/margin
			*/
			my: [{ my: scaleMargin() }],
			/**
			* Margin Inline Start
			* @see https://tailwindcss.com/docs/margin
			*/
			ms: [{ ms: scaleMargin() }],
			/**
			* Margin Inline End
			* @see https://tailwindcss.com/docs/margin
			*/
			me: [{ me: scaleMargin() }],
			/**
			* Margin Block Start
			* @see https://tailwindcss.com/docs/margin
			*/
			mbs: [{ mbs: scaleMargin() }],
			/**
			* Margin Block End
			* @see https://tailwindcss.com/docs/margin
			*/
			mbe: [{ mbe: scaleMargin() }],
			/**
			* Margin Top
			* @see https://tailwindcss.com/docs/margin
			*/
			mt: [{ mt: scaleMargin() }],
			/**
			* Margin Right
			* @see https://tailwindcss.com/docs/margin
			*/
			mr: [{ mr: scaleMargin() }],
			/**
			* Margin Bottom
			* @see https://tailwindcss.com/docs/margin
			*/
			mb: [{ mb: scaleMargin() }],
			/**
			* Margin Left
			* @see https://tailwindcss.com/docs/margin
			*/
			ml: [{ ml: scaleMargin() }],
			/**
			* Space Between X
			* @see https://tailwindcss.com/docs/margin#adding-space-between-children
			*/
			"space-x": [{ "space-x": scaleUnambiguousSpacing() }],
			/**
			* Space Between X Reverse
			* @see https://tailwindcss.com/docs/margin#adding-space-between-children
			*/
			"space-x-reverse": ["space-x-reverse"],
			/**
			* Space Between Y
			* @see https://tailwindcss.com/docs/margin#adding-space-between-children
			*/
			"space-y": [{ "space-y": scaleUnambiguousSpacing() }],
			/**
			* Space Between Y Reverse
			* @see https://tailwindcss.com/docs/margin#adding-space-between-children
			*/
			"space-y-reverse": ["space-y-reverse"],
			/**
			* Size
			* @see https://tailwindcss.com/docs/width#setting-both-width-and-height
			*/
			size: [{ size: scaleSizing() }],
			/**
			* Inline Size
			* @see https://tailwindcss.com/docs/width
			*/
			"inline-size": [{ inline: ["auto", ...scaleSizingInline()] }],
			/**
			* Min-Inline Size
			* @see https://tailwindcss.com/docs/min-width
			*/
			"min-inline-size": [{ "min-inline": ["auto", ...scaleSizingInline()] }],
			/**
			* Max-Inline Size
			* @see https://tailwindcss.com/docs/max-width
			*/
			"max-inline-size": [{ "max-inline": ["none", ...scaleSizingInline()] }],
			/**
			* Block Size
			* @see https://tailwindcss.com/docs/height
			*/
			"block-size": [{ block: ["auto", ...scaleSizingBlock()] }],
			/**
			* Min-Block Size
			* @see https://tailwindcss.com/docs/min-height
			*/
			"min-block-size": [{ "min-block": ["auto", ...scaleSizingBlock()] }],
			/**
			* Max-Block Size
			* @see https://tailwindcss.com/docs/max-height
			*/
			"max-block-size": [{ "max-block": ["none", ...scaleSizingBlock()] }],
			/**
			* Width
			* @see https://tailwindcss.com/docs/width
			*/
			w: [{ w: [
				themeContainer,
				"screen",
				...scaleSizing()
			] }],
			/**
			* Min-Width
			* @see https://tailwindcss.com/docs/min-width
			*/
			"min-w": [{ "min-w": [
				themeContainer,
				"screen",
				"none",
				...scaleSizing()
			] }],
			/**
			* Max-Width
			* @see https://tailwindcss.com/docs/max-width
			*/
			"max-w": [{ "max-w": [
				themeContainer,
				"screen",
				"none",
				"prose",
				{ screen: [themeBreakpoint] },
				...scaleSizing()
			] }],
			/**
			* Height
			* @see https://tailwindcss.com/docs/height
			*/
			h: [{ h: [
				"screen",
				"lh",
				...scaleSizing()
			] }],
			/**
			* Min-Height
			* @see https://tailwindcss.com/docs/min-height
			*/
			"min-h": [{ "min-h": [
				"screen",
				"lh",
				"none",
				...scaleSizing()
			] }],
			/**
			* Max-Height
			* @see https://tailwindcss.com/docs/max-height
			*/
			"max-h": [{ "max-h": [
				"screen",
				"lh",
				...scaleSizing()
			] }],
			/**
			* Font Size
			* @see https://tailwindcss.com/docs/font-size
			*/
			"font-size": [{ text: [
				"base",
				themeText,
				isArbitraryVariableLength,
				isArbitraryLength
			] }],
			/**
			* Font Smoothing
			* @see https://tailwindcss.com/docs/font-smoothing
			*/
			"font-smoothing": ["antialiased", "subpixel-antialiased"],
			/**
			* Font Style
			* @see https://tailwindcss.com/docs/font-style
			*/
			"font-style": ["italic", "not-italic"],
			/**
			* Font Weight
			* @see https://tailwindcss.com/docs/font-weight
			*/
			"font-weight": [{ font: [
				themeFontWeight,
				isArbitraryVariableWeight,
				isArbitraryWeight
			] }],
			/**
			* Font Stretch
			* @see https://tailwindcss.com/docs/font-stretch
			*/
			"font-stretch": [{ "font-stretch": [
				"ultra-condensed",
				"extra-condensed",
				"condensed",
				"semi-condensed",
				"normal",
				"semi-expanded",
				"expanded",
				"extra-expanded",
				"ultra-expanded",
				isPercent,
				isArbitraryValue
			] }],
			/**
			* Font Family
			* @see https://tailwindcss.com/docs/font-family
			*/
			"font-family": [{ font: [
				isArbitraryVariableFamilyName,
				isArbitraryFamilyName,
				themeFont
			] }],
			/**
			* Font Feature Settings
			* @see https://tailwindcss.com/docs/font-feature-settings
			*/
			"font-features": [{ "font-features": [isArbitraryValue] }],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-normal": ["normal-nums"],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-ordinal": ["ordinal"],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-slashed-zero": ["slashed-zero"],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-figure": ["lining-nums", "oldstyle-nums"],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-spacing": ["proportional-nums", "tabular-nums"],
			/**
			* Font Variant Numeric
			* @see https://tailwindcss.com/docs/font-variant-numeric
			*/
			"fvn-fraction": ["diagonal-fractions", "stacked-fractions"],
			/**
			* Letter Spacing
			* @see https://tailwindcss.com/docs/letter-spacing
			*/
			tracking: [{ tracking: [
				themeTracking,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Line Clamp
			* @see https://tailwindcss.com/docs/line-clamp
			*/
			"line-clamp": [{ "line-clamp": [
				isNumber,
				"none",
				isArbitraryVariable,
				isArbitraryNumber
			] }],
			/**
			* Line Height
			* @see https://tailwindcss.com/docs/line-height
			*/
			leading: [{ leading: [themeLeading, ...scaleUnambiguousSpacing()] }],
			/**
			* List Style Image
			* @see https://tailwindcss.com/docs/list-style-image
			*/
			"list-image": [{ "list-image": [
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* List Style Position
			* @see https://tailwindcss.com/docs/list-style-position
			*/
			"list-style-position": [{ list: ["inside", "outside"] }],
			/**
			* List Style Type
			* @see https://tailwindcss.com/docs/list-style-type
			*/
			"list-style-type": [{ list: [
				"disc",
				"decimal",
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Text Alignment
			* @see https://tailwindcss.com/docs/text-align
			*/
			"text-alignment": [{ text: [
				"left",
				"center",
				"right",
				"justify",
				"start",
				"end"
			] }],
			/**
			* Placeholder Color
			* @deprecated since Tailwind CSS v3.0.0
			* @see https://v3.tailwindcss.com/docs/placeholder-color
			*/
			"placeholder-color": [{ placeholder: scaleColor() }],
			/**
			* Text Color
			* @see https://tailwindcss.com/docs/text-color
			*/
			"text-color": [{ text: scaleColor() }],
			/**
			* Text Decoration
			* @see https://tailwindcss.com/docs/text-decoration
			*/
			"text-decoration": [
				"underline",
				"overline",
				"line-through",
				"no-underline"
			],
			/**
			* Text Decoration Style
			* @see https://tailwindcss.com/docs/text-decoration-style
			*/
			"text-decoration-style": [{ decoration: [...scaleLineStyle(), "wavy"] }],
			/**
			* Text Decoration Thickness
			* @see https://tailwindcss.com/docs/text-decoration-thickness
			*/
			"text-decoration-thickness": [{ decoration: [
				isNumber,
				"from-font",
				"auto",
				isArbitraryVariable,
				isArbitraryLength
			] }],
			/**
			* Text Decoration Color
			* @see https://tailwindcss.com/docs/text-decoration-color
			*/
			"text-decoration-color": [{ decoration: scaleColor() }],
			/**
			* Text Underline Offset
			* @see https://tailwindcss.com/docs/text-underline-offset
			*/
			"underline-offset": [{ "underline-offset": [
				isNumber,
				"auto",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Text Transform
			* @see https://tailwindcss.com/docs/text-transform
			*/
			"text-transform": [
				"uppercase",
				"lowercase",
				"capitalize",
				"normal-case"
			],
			/**
			* Text Overflow
			* @see https://tailwindcss.com/docs/text-overflow
			*/
			"text-overflow": [
				"truncate",
				"text-ellipsis",
				"text-clip"
			],
			/**
			* Text Wrap
			* @see https://tailwindcss.com/docs/text-wrap
			*/
			"text-wrap": [{ text: [
				"wrap",
				"nowrap",
				"balance",
				"pretty"
			] }],
			/**
			* Text Indent
			* @see https://tailwindcss.com/docs/text-indent
			*/
			indent: [{ indent: scaleUnambiguousSpacing() }],
			/**
			* Tab Size
			* @see https://tailwindcss.com/docs/tab-size
			*/
			"tab-size": [{ tab: [
				isInteger,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Vertical Alignment
			* @see https://tailwindcss.com/docs/vertical-align
			*/
			"vertical-align": [{ align: [
				"baseline",
				"top",
				"middle",
				"bottom",
				"text-top",
				"text-bottom",
				"sub",
				"super",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Whitespace
			* @see https://tailwindcss.com/docs/whitespace
			*/
			whitespace: [{ whitespace: [
				"normal",
				"nowrap",
				"pre",
				"pre-line",
				"pre-wrap",
				"break-spaces"
			] }],
			/**
			* Word Break
			* @see https://tailwindcss.com/docs/word-break
			*/
			break: [{ break: [
				"normal",
				"words",
				"all",
				"keep"
			] }],
			/**
			* Overflow Wrap
			* @see https://tailwindcss.com/docs/overflow-wrap
			*/
			wrap: [{ wrap: [
				"break-word",
				"anywhere",
				"normal"
			] }],
			/**
			* Hyphens
			* @see https://tailwindcss.com/docs/hyphens
			*/
			hyphens: [{ hyphens: [
				"none",
				"manual",
				"auto"
			] }],
			/**
			* Content
			* @see https://tailwindcss.com/docs/content
			*/
			content: [{ content: [
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Background Attachment
			* @see https://tailwindcss.com/docs/background-attachment
			*/
			"bg-attachment": [{ bg: [
				"fixed",
				"local",
				"scroll"
			] }],
			/**
			* Background Clip
			* @see https://tailwindcss.com/docs/background-clip
			*/
			"bg-clip": [{ "bg-clip": [
				"border",
				"padding",
				"content",
				"text"
			] }],
			/**
			* Background Origin
			* @see https://tailwindcss.com/docs/background-origin
			*/
			"bg-origin": [{ "bg-origin": [
				"border",
				"padding",
				"content"
			] }],
			/**
			* Background Position
			* @see https://tailwindcss.com/docs/background-position
			*/
			"bg-position": [{ bg: scaleBgPosition() }],
			/**
			* Background Repeat
			* @see https://tailwindcss.com/docs/background-repeat
			*/
			"bg-repeat": [{ bg: scaleBgRepeat() }],
			/**
			* Background Size
			* @see https://tailwindcss.com/docs/background-size
			*/
			"bg-size": [{ bg: scaleBgSize() }],
			/**
			* Background Image
			* @see https://tailwindcss.com/docs/background-image
			*/
			"bg-image": [{ bg: [
				"none",
				{
					linear: [
						{ to: [
							"t",
							"tr",
							"r",
							"br",
							"b",
							"bl",
							"l",
							"tl"
						] },
						isInteger,
						isArbitraryVariable,
						isArbitraryValue
					],
					radial: [
						"",
						isArbitraryVariable,
						isArbitraryValue
					],
					conic: [
						isInteger,
						isArbitraryVariable,
						isArbitraryValue
					]
				},
				isArbitraryVariableImage,
				isArbitraryImage
			] }],
			/**
			* Background Color
			* @see https://tailwindcss.com/docs/background-color
			*/
			"bg-color": [{ bg: scaleColor() }],
			/**
			* Gradient Color Stops From Position
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-from-pos": [{ from: scaleGradientStopPosition() }],
			/**
			* Gradient Color Stops Via Position
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-via-pos": [{ via: scaleGradientStopPosition() }],
			/**
			* Gradient Color Stops To Position
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-to-pos": [{ to: scaleGradientStopPosition() }],
			/**
			* Gradient Color Stops From
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-from": [{ from: scaleColor() }],
			/**
			* Gradient Color Stops Via
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-via": [{ via: scaleColor() }],
			/**
			* Gradient Color Stops To
			* @see https://tailwindcss.com/docs/gradient-color-stops
			*/
			"gradient-to": [{ to: scaleColor() }],
			/**
			* Border Radius
			* @see https://tailwindcss.com/docs/border-radius
			*/
			rounded: [{ rounded: scaleRadius() }],
			/**
			* Border Radius Start
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-s": [{ "rounded-s": scaleRadius() }],
			/**
			* Border Radius End
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-e": [{ "rounded-e": scaleRadius() }],
			/**
			* Border Radius Top
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-t": [{ "rounded-t": scaleRadius() }],
			/**
			* Border Radius Right
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-r": [{ "rounded-r": scaleRadius() }],
			/**
			* Border Radius Bottom
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-b": [{ "rounded-b": scaleRadius() }],
			/**
			* Border Radius Left
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-l": [{ "rounded-l": scaleRadius() }],
			/**
			* Border Radius Start Start
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-ss": [{ "rounded-ss": scaleRadius() }],
			/**
			* Border Radius Start End
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-se": [{ "rounded-se": scaleRadius() }],
			/**
			* Border Radius End End
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-ee": [{ "rounded-ee": scaleRadius() }],
			/**
			* Border Radius End Start
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-es": [{ "rounded-es": scaleRadius() }],
			/**
			* Border Radius Top Left
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-tl": [{ "rounded-tl": scaleRadius() }],
			/**
			* Border Radius Top Right
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-tr": [{ "rounded-tr": scaleRadius() }],
			/**
			* Border Radius Bottom Right
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-br": [{ "rounded-br": scaleRadius() }],
			/**
			* Border Radius Bottom Left
			* @see https://tailwindcss.com/docs/border-radius
			*/
			"rounded-bl": [{ "rounded-bl": scaleRadius() }],
			/**
			* Border Width
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w": [{ border: scaleBorderWidth() }],
			/**
			* Border Width Inline
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-x": [{ "border-x": scaleBorderWidth() }],
			/**
			* Border Width Block
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-y": [{ "border-y": scaleBorderWidth() }],
			/**
			* Border Width Inline Start
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-s": [{ "border-s": scaleBorderWidth() }],
			/**
			* Border Width Inline End
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-e": [{ "border-e": scaleBorderWidth() }],
			/**
			* Border Width Block Start
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-bs": [{ "border-bs": scaleBorderWidth() }],
			/**
			* Border Width Block End
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-be": [{ "border-be": scaleBorderWidth() }],
			/**
			* Border Width Top
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-t": [{ "border-t": scaleBorderWidth() }],
			/**
			* Border Width Right
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-r": [{ "border-r": scaleBorderWidth() }],
			/**
			* Border Width Bottom
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-b": [{ "border-b": scaleBorderWidth() }],
			/**
			* Border Width Left
			* @see https://tailwindcss.com/docs/border-width
			*/
			"border-w-l": [{ "border-l": scaleBorderWidth() }],
			/**
			* Divide Width X
			* @see https://tailwindcss.com/docs/border-width#between-children
			*/
			"divide-x": [{ "divide-x": scaleBorderWidth() }],
			/**
			* Divide Width X Reverse
			* @see https://tailwindcss.com/docs/border-width#between-children
			*/
			"divide-x-reverse": ["divide-x-reverse"],
			/**
			* Divide Width Y
			* @see https://tailwindcss.com/docs/border-width#between-children
			*/
			"divide-y": [{ "divide-y": scaleBorderWidth() }],
			/**
			* Divide Width Y Reverse
			* @see https://tailwindcss.com/docs/border-width#between-children
			*/
			"divide-y-reverse": ["divide-y-reverse"],
			/**
			* Border Style
			* @see https://tailwindcss.com/docs/border-style
			*/
			"border-style": [{ border: [
				...scaleLineStyle(),
				"hidden",
				"none"
			] }],
			/**
			* Divide Style
			* @see https://tailwindcss.com/docs/border-style#setting-the-divider-style
			*/
			"divide-style": [{ divide: [
				...scaleLineStyle(),
				"hidden",
				"none"
			] }],
			/**
			* Border Color
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color": [{ border: scaleColor() }],
			/**
			* Border Color Inline
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-x": [{ "border-x": scaleColor() }],
			/**
			* Border Color Block
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-y": [{ "border-y": scaleColor() }],
			/**
			* Border Color Inline Start
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-s": [{ "border-s": scaleColor() }],
			/**
			* Border Color Inline End
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-e": [{ "border-e": scaleColor() }],
			/**
			* Border Color Block Start
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-bs": [{ "border-bs": scaleColor() }],
			/**
			* Border Color Block End
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-be": [{ "border-be": scaleColor() }],
			/**
			* Border Color Top
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-t": [{ "border-t": scaleColor() }],
			/**
			* Border Color Right
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-r": [{ "border-r": scaleColor() }],
			/**
			* Border Color Bottom
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-b": [{ "border-b": scaleColor() }],
			/**
			* Border Color Left
			* @see https://tailwindcss.com/docs/border-color
			*/
			"border-color-l": [{ "border-l": scaleColor() }],
			/**
			* Divide Color
			* @see https://tailwindcss.com/docs/divide-color
			*/
			"divide-color": [{ divide: scaleColor() }],
			/**
			* Outline Style
			* @see https://tailwindcss.com/docs/outline-style
			*/
			"outline-style": [{ outline: [
				...scaleLineStyle(),
				"none",
				"hidden"
			] }],
			/**
			* Outline Offset
			* @see https://tailwindcss.com/docs/outline-offset
			*/
			"outline-offset": [{ "outline-offset": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Outline Width
			* @see https://tailwindcss.com/docs/outline-width
			*/
			"outline-w": [{ outline: [
				"",
				isNumber,
				isArbitraryVariableLength,
				isArbitraryLength
			] }],
			/**
			* Outline Color
			* @see https://tailwindcss.com/docs/outline-color
			*/
			"outline-color": [{ outline: scaleColor() }],
			/**
			* Box Shadow
			* @see https://tailwindcss.com/docs/box-shadow
			*/
			shadow: [{ shadow: [
				"",
				"none",
				themeShadow,
				isArbitraryVariableShadow,
				isArbitraryShadow
			] }],
			/**
			* Box Shadow Color
			* @see https://tailwindcss.com/docs/box-shadow#setting-the-shadow-color
			*/
			"shadow-color": [{ shadow: scaleColor() }],
			/**
			* Inset Box Shadow
			* @see https://tailwindcss.com/docs/box-shadow#adding-an-inset-shadow
			*/
			"inset-shadow": [{ "inset-shadow": [
				"none",
				themeInsetShadow,
				isArbitraryVariableShadow,
				isArbitraryShadow
			] }],
			/**
			* Inset Box Shadow Color
			* @see https://tailwindcss.com/docs/box-shadow#setting-the-inset-shadow-color
			*/
			"inset-shadow-color": [{ "inset-shadow": scaleColor() }],
			/**
			* Ring Width
			* @see https://tailwindcss.com/docs/box-shadow#adding-a-ring
			*/
			"ring-w": [{ ring: scaleBorderWidth() }],
			/**
			* Ring Width Inset
			* @see https://v3.tailwindcss.com/docs/ring-width#inset-rings
			* @deprecated since Tailwind CSS v4.0.0
			* @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
			*/
			"ring-w-inset": ["ring-inset"],
			/**
			* Ring Color
			* @see https://tailwindcss.com/docs/box-shadow#setting-the-ring-color
			*/
			"ring-color": [{ ring: scaleColor() }],
			/**
			* Ring Offset Width
			* @see https://v3.tailwindcss.com/docs/ring-offset-width
			* @deprecated since Tailwind CSS v4.0.0
			* @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
			*/
			"ring-offset-w": [{ "ring-offset": [isNumber, isArbitraryLength] }],
			/**
			* Ring Offset Color
			* @see https://v3.tailwindcss.com/docs/ring-offset-color
			* @deprecated since Tailwind CSS v4.0.0
			* @see https://github.com/tailwindlabs/tailwindcss/blob/v4.0.0/packages/tailwindcss/src/utilities.ts#L4158
			*/
			"ring-offset-color": [{ "ring-offset": scaleColor() }],
			/**
			* Inset Ring Width
			* @see https://tailwindcss.com/docs/box-shadow#adding-an-inset-ring
			*/
			"inset-ring-w": [{ "inset-ring": scaleBorderWidth() }],
			/**
			* Inset Ring Color
			* @see https://tailwindcss.com/docs/box-shadow#setting-the-inset-ring-color
			*/
			"inset-ring-color": [{ "inset-ring": scaleColor() }],
			/**
			* Text Shadow
			* @see https://tailwindcss.com/docs/text-shadow
			*/
			"text-shadow": [{ "text-shadow": [
				"none",
				themeTextShadow,
				isArbitraryVariableShadow,
				isArbitraryShadow
			] }],
			/**
			* Text Shadow Color
			* @see https://tailwindcss.com/docs/text-shadow#setting-the-shadow-color
			*/
			"text-shadow-color": [{ "text-shadow": scaleColor() }],
			/**
			* Opacity
			* @see https://tailwindcss.com/docs/opacity
			*/
			opacity: [{ opacity: [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Mix Blend Mode
			* @see https://tailwindcss.com/docs/mix-blend-mode
			*/
			"mix-blend": [{ "mix-blend": [
				...scaleBlendMode(),
				"plus-darker",
				"plus-lighter"
			] }],
			/**
			* Background Blend Mode
			* @see https://tailwindcss.com/docs/background-blend-mode
			*/
			"bg-blend": [{ "bg-blend": scaleBlendMode() }],
			/**
			* Mask Clip
			* @see https://tailwindcss.com/docs/mask-clip
			*/
			"mask-clip": [{ "mask-clip": [
				"border",
				"padding",
				"content",
				"fill",
				"stroke",
				"view"
			] }, "mask-no-clip"],
			/**
			* Mask Composite
			* @see https://tailwindcss.com/docs/mask-composite
			*/
			"mask-composite": [{ mask: [
				"add",
				"subtract",
				"intersect",
				"exclude"
			] }],
			/**
			* Mask Image
			* @see https://tailwindcss.com/docs/mask-image
			*/
			"mask-image-linear-pos": [{ "mask-linear": [isNumber] }],
			"mask-image-linear-from-pos": [{ "mask-linear-from": scaleMaskImagePosition() }],
			"mask-image-linear-to-pos": [{ "mask-linear-to": scaleMaskImagePosition() }],
			"mask-image-linear-from-color": [{ "mask-linear-from": scaleColor() }],
			"mask-image-linear-to-color": [{ "mask-linear-to": scaleColor() }],
			"mask-image-t-from-pos": [{ "mask-t-from": scaleMaskImagePosition() }],
			"mask-image-t-to-pos": [{ "mask-t-to": scaleMaskImagePosition() }],
			"mask-image-t-from-color": [{ "mask-t-from": scaleColor() }],
			"mask-image-t-to-color": [{ "mask-t-to": scaleColor() }],
			"mask-image-r-from-pos": [{ "mask-r-from": scaleMaskImagePosition() }],
			"mask-image-r-to-pos": [{ "mask-r-to": scaleMaskImagePosition() }],
			"mask-image-r-from-color": [{ "mask-r-from": scaleColor() }],
			"mask-image-r-to-color": [{ "mask-r-to": scaleColor() }],
			"mask-image-b-from-pos": [{ "mask-b-from": scaleMaskImagePosition() }],
			"mask-image-b-to-pos": [{ "mask-b-to": scaleMaskImagePosition() }],
			"mask-image-b-from-color": [{ "mask-b-from": scaleColor() }],
			"mask-image-b-to-color": [{ "mask-b-to": scaleColor() }],
			"mask-image-l-from-pos": [{ "mask-l-from": scaleMaskImagePosition() }],
			"mask-image-l-to-pos": [{ "mask-l-to": scaleMaskImagePosition() }],
			"mask-image-l-from-color": [{ "mask-l-from": scaleColor() }],
			"mask-image-l-to-color": [{ "mask-l-to": scaleColor() }],
			"mask-image-x-from-pos": [{ "mask-x-from": scaleMaskImagePosition() }],
			"mask-image-x-to-pos": [{ "mask-x-to": scaleMaskImagePosition() }],
			"mask-image-x-from-color": [{ "mask-x-from": scaleColor() }],
			"mask-image-x-to-color": [{ "mask-x-to": scaleColor() }],
			"mask-image-y-from-pos": [{ "mask-y-from": scaleMaskImagePosition() }],
			"mask-image-y-to-pos": [{ "mask-y-to": scaleMaskImagePosition() }],
			"mask-image-y-from-color": [{ "mask-y-from": scaleColor() }],
			"mask-image-y-to-color": [{ "mask-y-to": scaleColor() }],
			"mask-image-radial": [{ "mask-radial": [isArbitraryVariable, isArbitraryValue] }],
			"mask-image-radial-from-pos": [{ "mask-radial-from": scaleMaskImagePosition() }],
			"mask-image-radial-to-pos": [{ "mask-radial-to": scaleMaskImagePosition() }],
			"mask-image-radial-from-color": [{ "mask-radial-from": scaleColor() }],
			"mask-image-radial-to-color": [{ "mask-radial-to": scaleColor() }],
			"mask-image-radial-shape": [{ "mask-radial": ["circle", "ellipse"] }],
			"mask-image-radial-size": [{ "mask-radial": [{
				closest: ["side", "corner"],
				farthest: ["side", "corner"]
			}] }],
			"mask-image-radial-pos": [{ "mask-radial-at": scalePosition() }],
			"mask-image-conic-pos": [{ "mask-conic": [isNumber] }],
			"mask-image-conic-from-pos": [{ "mask-conic-from": scaleMaskImagePosition() }],
			"mask-image-conic-to-pos": [{ "mask-conic-to": scaleMaskImagePosition() }],
			"mask-image-conic-from-color": [{ "mask-conic-from": scaleColor() }],
			"mask-image-conic-to-color": [{ "mask-conic-to": scaleColor() }],
			/**
			* Mask Mode
			* @see https://tailwindcss.com/docs/mask-mode
			*/
			"mask-mode": [{ mask: [
				"alpha",
				"luminance",
				"match"
			] }],
			/**
			* Mask Origin
			* @see https://tailwindcss.com/docs/mask-origin
			*/
			"mask-origin": [{ "mask-origin": [
				"border",
				"padding",
				"content",
				"fill",
				"stroke",
				"view"
			] }],
			/**
			* Mask Position
			* @see https://tailwindcss.com/docs/mask-position
			*/
			"mask-position": [{ mask: scaleBgPosition() }],
			/**
			* Mask Repeat
			* @see https://tailwindcss.com/docs/mask-repeat
			*/
			"mask-repeat": [{ mask: scaleBgRepeat() }],
			/**
			* Mask Size
			* @see https://tailwindcss.com/docs/mask-size
			*/
			"mask-size": [{ mask: scaleBgSize() }],
			/**
			* Mask Type
			* @see https://tailwindcss.com/docs/mask-type
			*/
			"mask-type": [{ "mask-type": ["alpha", "luminance"] }],
			/**
			* Mask Image
			* @see https://tailwindcss.com/docs/mask-image
			*/
			"mask-image": [{ mask: [
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Filter
			* @see https://tailwindcss.com/docs/filter
			*/
			filter: [{ filter: [
				"",
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Blur
			* @see https://tailwindcss.com/docs/blur
			*/
			blur: [{ blur: scaleBlur() }],
			/**
			* Brightness
			* @see https://tailwindcss.com/docs/brightness
			*/
			brightness: [{ brightness: [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Contrast
			* @see https://tailwindcss.com/docs/contrast
			*/
			contrast: [{ contrast: [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Drop Shadow
			* @see https://tailwindcss.com/docs/drop-shadow
			*/
			"drop-shadow": [{ "drop-shadow": [
				"",
				"none",
				themeDropShadow,
				isArbitraryVariableShadow,
				isArbitraryShadow
			] }],
			/**
			* Drop Shadow Color
			* @see https://tailwindcss.com/docs/filter-drop-shadow#setting-the-shadow-color
			*/
			"drop-shadow-color": [{ "drop-shadow": scaleColor() }],
			/**
			* Grayscale
			* @see https://tailwindcss.com/docs/grayscale
			*/
			grayscale: [{ grayscale: [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Hue Rotate
			* @see https://tailwindcss.com/docs/hue-rotate
			*/
			"hue-rotate": [{ "hue-rotate": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Invert
			* @see https://tailwindcss.com/docs/invert
			*/
			invert: [{ invert: [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Saturate
			* @see https://tailwindcss.com/docs/saturate
			*/
			saturate: [{ saturate: [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Sepia
			* @see https://tailwindcss.com/docs/sepia
			*/
			sepia: [{ sepia: [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Filter
			* @see https://tailwindcss.com/docs/backdrop-filter
			*/
			"backdrop-filter": [{ "backdrop-filter": [
				"",
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Blur
			* @see https://tailwindcss.com/docs/backdrop-blur
			*/
			"backdrop-blur": [{ "backdrop-blur": scaleBlur() }],
			/**
			* Backdrop Brightness
			* @see https://tailwindcss.com/docs/backdrop-brightness
			*/
			"backdrop-brightness": [{ "backdrop-brightness": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Contrast
			* @see https://tailwindcss.com/docs/backdrop-contrast
			*/
			"backdrop-contrast": [{ "backdrop-contrast": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Grayscale
			* @see https://tailwindcss.com/docs/backdrop-grayscale
			*/
			"backdrop-grayscale": [{ "backdrop-grayscale": [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Hue Rotate
			* @see https://tailwindcss.com/docs/backdrop-hue-rotate
			*/
			"backdrop-hue-rotate": [{ "backdrop-hue-rotate": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Invert
			* @see https://tailwindcss.com/docs/backdrop-invert
			*/
			"backdrop-invert": [{ "backdrop-invert": [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Opacity
			* @see https://tailwindcss.com/docs/backdrop-opacity
			*/
			"backdrop-opacity": [{ "backdrop-opacity": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Saturate
			* @see https://tailwindcss.com/docs/backdrop-saturate
			*/
			"backdrop-saturate": [{ "backdrop-saturate": [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backdrop Sepia
			* @see https://tailwindcss.com/docs/backdrop-sepia
			*/
			"backdrop-sepia": [{ "backdrop-sepia": [
				"",
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Border Collapse
			* @see https://tailwindcss.com/docs/border-collapse
			*/
			"border-collapse": [{ border: ["collapse", "separate"] }],
			/**
			* Border Spacing
			* @see https://tailwindcss.com/docs/border-spacing
			*/
			"border-spacing": [{ "border-spacing": scaleUnambiguousSpacing() }],
			/**
			* Border Spacing X
			* @see https://tailwindcss.com/docs/border-spacing
			*/
			"border-spacing-x": [{ "border-spacing-x": scaleUnambiguousSpacing() }],
			/**
			* Border Spacing Y
			* @see https://tailwindcss.com/docs/border-spacing
			*/
			"border-spacing-y": [{ "border-spacing-y": scaleUnambiguousSpacing() }],
			/**
			* Table Layout
			* @see https://tailwindcss.com/docs/table-layout
			*/
			"table-layout": [{ table: ["auto", "fixed"] }],
			/**
			* Caption Side
			* @see https://tailwindcss.com/docs/caption-side
			*/
			caption: [{ caption: ["top", "bottom"] }],
			/**
			* Transition Property
			* @see https://tailwindcss.com/docs/transition-property
			*/
			transition: [{ transition: [
				"",
				"all",
				"colors",
				"opacity",
				"shadow",
				"transform",
				"none",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Transition Behavior
			* @see https://tailwindcss.com/docs/transition-behavior
			*/
			"transition-behavior": [{ transition: ["normal", "discrete"] }],
			/**
			* Transition Duration
			* @see https://tailwindcss.com/docs/transition-duration
			*/
			duration: [{ duration: [
				isNumber,
				"initial",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Transition Timing Function
			* @see https://tailwindcss.com/docs/transition-timing-function
			*/
			ease: [{ ease: [
				"linear",
				"initial",
				themeEase,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Transition Delay
			* @see https://tailwindcss.com/docs/transition-delay
			*/
			delay: [{ delay: [
				isNumber,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Animation
			* @see https://tailwindcss.com/docs/animation
			*/
			animate: [{ animate: [
				"none",
				themeAnimate,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Backface Visibility
			* @see https://tailwindcss.com/docs/backface-visibility
			*/
			backface: [{ backface: ["hidden", "visible"] }],
			/**
			* Perspective
			* @see https://tailwindcss.com/docs/perspective
			*/
			perspective: [{ perspective: [
				themePerspective,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Perspective Origin
			* @see https://tailwindcss.com/docs/perspective-origin
			*/
			"perspective-origin": [{ "perspective-origin": scalePositionWithArbitrary() }],
			/**
			* Rotate
			* @see https://tailwindcss.com/docs/rotate
			*/
			rotate: [{ rotate: scaleRotate() }],
			/**
			* Rotate X
			* @see https://tailwindcss.com/docs/rotate
			*/
			"rotate-x": [{ "rotate-x": scaleRotate() }],
			/**
			* Rotate Y
			* @see https://tailwindcss.com/docs/rotate
			*/
			"rotate-y": [{ "rotate-y": scaleRotate() }],
			/**
			* Rotate Z
			* @see https://tailwindcss.com/docs/rotate
			*/
			"rotate-z": [{ "rotate-z": scaleRotate() }],
			/**
			* Scale
			* @see https://tailwindcss.com/docs/scale
			*/
			scale: [{ scale: scaleScale() }],
			/**
			* Scale X
			* @see https://tailwindcss.com/docs/scale
			*/
			"scale-x": [{ "scale-x": scaleScale() }],
			/**
			* Scale Y
			* @see https://tailwindcss.com/docs/scale
			*/
			"scale-y": [{ "scale-y": scaleScale() }],
			/**
			* Scale Z
			* @see https://tailwindcss.com/docs/scale
			*/
			"scale-z": [{ "scale-z": scaleScale() }],
			/**
			* Scale 3D
			* @see https://tailwindcss.com/docs/scale
			*/
			"scale-3d": ["scale-3d"],
			/**
			* Skew
			* @see https://tailwindcss.com/docs/skew
			*/
			skew: [{ skew: scaleSkew() }],
			/**
			* Skew X
			* @see https://tailwindcss.com/docs/skew
			*/
			"skew-x": [{ "skew-x": scaleSkew() }],
			/**
			* Skew Y
			* @see https://tailwindcss.com/docs/skew
			*/
			"skew-y": [{ "skew-y": scaleSkew() }],
			/**
			* Transform
			* @see https://tailwindcss.com/docs/transform
			*/
			transform: [{ transform: [
				isArbitraryVariable,
				isArbitraryValue,
				"",
				"none",
				"gpu",
				"cpu"
			] }],
			/**
			* Transform Origin
			* @see https://tailwindcss.com/docs/transform-origin
			*/
			"transform-origin": [{ origin: scalePositionWithArbitrary() }],
			/**
			* Transform Style
			* @see https://tailwindcss.com/docs/transform-style
			*/
			"transform-style": [{ transform: ["3d", "flat"] }],
			/**
			* Translate
			* @see https://tailwindcss.com/docs/translate
			*/
			translate: [{ translate: scaleTranslate() }],
			/**
			* Translate X
			* @see https://tailwindcss.com/docs/translate
			*/
			"translate-x": [{ "translate-x": scaleTranslate() }],
			/**
			* Translate Y
			* @see https://tailwindcss.com/docs/translate
			*/
			"translate-y": [{ "translate-y": scaleTranslate() }],
			/**
			* Translate Z
			* @see https://tailwindcss.com/docs/translate
			*/
			"translate-z": [{ "translate-z": scaleTranslate() }],
			/**
			* Translate None
			* @see https://tailwindcss.com/docs/translate
			*/
			"translate-none": ["translate-none"],
			/**
			* Zoom
			* @see https://tailwindcss.com/docs/zoom
			*/
			zoom: [{ zoom: [
				isInteger,
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Accent Color
			* @see https://tailwindcss.com/docs/accent-color
			*/
			accent: [{ accent: scaleColor() }],
			/**
			* Appearance
			* @see https://tailwindcss.com/docs/appearance
			*/
			appearance: [{ appearance: ["none", "auto"] }],
			/**
			* Caret Color
			* @see https://tailwindcss.com/docs/just-in-time-mode#caret-color-utilities
			*/
			"caret-color": [{ caret: scaleColor() }],
			/**
			* Color Scheme
			* @see https://tailwindcss.com/docs/color-scheme
			*/
			"color-scheme": [{ scheme: [
				"normal",
				"dark",
				"light",
				"light-dark",
				"only-dark",
				"only-light"
			] }],
			/**
			* Cursor
			* @see https://tailwindcss.com/docs/cursor
			*/
			cursor: [{ cursor: [
				"auto",
				"default",
				"pointer",
				"wait",
				"text",
				"move",
				"help",
				"not-allowed",
				"none",
				"context-menu",
				"progress",
				"cell",
				"crosshair",
				"vertical-text",
				"alias",
				"copy",
				"no-drop",
				"grab",
				"grabbing",
				"all-scroll",
				"col-resize",
				"row-resize",
				"n-resize",
				"e-resize",
				"s-resize",
				"w-resize",
				"ne-resize",
				"nw-resize",
				"se-resize",
				"sw-resize",
				"ew-resize",
				"ns-resize",
				"nesw-resize",
				"nwse-resize",
				"zoom-in",
				"zoom-out",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Field Sizing
			* @see https://tailwindcss.com/docs/field-sizing
			*/
			"field-sizing": [{ "field-sizing": ["fixed", "content"] }],
			/**
			* Pointer Events
			* @see https://tailwindcss.com/docs/pointer-events
			*/
			"pointer-events": [{ "pointer-events": ["auto", "none"] }],
			/**
			* Resize
			* @see https://tailwindcss.com/docs/resize
			*/
			resize: [{ resize: [
				"none",
				"",
				"y",
				"x"
			] }],
			/**
			* Scroll Behavior
			* @see https://tailwindcss.com/docs/scroll-behavior
			*/
			"scroll-behavior": [{ scroll: ["auto", "smooth"] }],
			/**
			* Scrollbar Thumb Color
			* @see https://tailwindcss.com/docs/scrollbar-color
			*/
			"scrollbar-thumb-color": [{ "scrollbar-thumb": scaleColor() }],
			/**
			* Scrollbar Track Color
			* @see https://tailwindcss.com/docs/scrollbar-color
			*/
			"scrollbar-track-color": [{ "scrollbar-track": scaleColor() }],
			/**
			* Scrollbar Gutter
			* @see https://tailwindcss.com/docs/scrollbar-gutter
			*/
			"scrollbar-gutter": [{ "scrollbar-gutter": [
				"auto",
				"stable",
				"both"
			] }],
			/**
			* Scrollbar Width
			* @see https://tailwindcss.com/docs/scrollbar-width
			*/
			"scrollbar-w": [{ scrollbar: [
				"auto",
				"thin",
				"none"
			] }],
			/**
			* Scroll Margin
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-m": [{ "scroll-m": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Inline
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mx": [{ "scroll-mx": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Block
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-my": [{ "scroll-my": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Inline Start
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-ms": [{ "scroll-ms": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Inline End
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-me": [{ "scroll-me": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Block Start
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mbs": [{ "scroll-mbs": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Block End
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mbe": [{ "scroll-mbe": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Top
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mt": [{ "scroll-mt": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Right
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mr": [{ "scroll-mr": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Bottom
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-mb": [{ "scroll-mb": scaleUnambiguousSpacing() }],
			/**
			* Scroll Margin Left
			* @see https://tailwindcss.com/docs/scroll-margin
			*/
			"scroll-ml": [{ "scroll-ml": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-p": [{ "scroll-p": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Inline
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-px": [{ "scroll-px": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Block
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-py": [{ "scroll-py": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Inline Start
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-ps": [{ "scroll-ps": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Inline End
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pe": [{ "scroll-pe": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Block Start
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pbs": [{ "scroll-pbs": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Block End
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pbe": [{ "scroll-pbe": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Top
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pt": [{ "scroll-pt": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Right
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pr": [{ "scroll-pr": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Bottom
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pb": [{ "scroll-pb": scaleUnambiguousSpacing() }],
			/**
			* Scroll Padding Left
			* @see https://tailwindcss.com/docs/scroll-padding
			*/
			"scroll-pl": [{ "scroll-pl": scaleUnambiguousSpacing() }],
			/**
			* Scroll Snap Align
			* @see https://tailwindcss.com/docs/scroll-snap-align
			*/
			"snap-align": [{ snap: [
				"start",
				"end",
				"center",
				"align-none"
			] }],
			/**
			* Scroll Snap Stop
			* @see https://tailwindcss.com/docs/scroll-snap-stop
			*/
			"snap-stop": [{ snap: ["normal", "always"] }],
			/**
			* Scroll Snap Type
			* @see https://tailwindcss.com/docs/scroll-snap-type
			*/
			"snap-type": [{ snap: [
				"none",
				"x",
				"y",
				"both"
			] }],
			/**
			* Scroll Snap Type Strictness
			* @see https://tailwindcss.com/docs/scroll-snap-type
			*/
			"snap-strictness": [{ snap: ["mandatory", "proximity"] }],
			/**
			* Touch Action
			* @see https://tailwindcss.com/docs/touch-action
			*/
			touch: [{ touch: [
				"auto",
				"none",
				"manipulation"
			] }],
			/**
			* Touch Action X
			* @see https://tailwindcss.com/docs/touch-action
			*/
			"touch-x": [{ "touch-pan": [
				"x",
				"left",
				"right"
			] }],
			/**
			* Touch Action Y
			* @see https://tailwindcss.com/docs/touch-action
			*/
			"touch-y": [{ "touch-pan": [
				"y",
				"up",
				"down"
			] }],
			/**
			* Touch Action Pinch Zoom
			* @see https://tailwindcss.com/docs/touch-action
			*/
			"touch-pz": ["touch-pinch-zoom"],
			/**
			* User Select
			* @see https://tailwindcss.com/docs/user-select
			*/
			select: [{ select: [
				"none",
				"text",
				"all",
				"auto"
			] }],
			/**
			* Will Change
			* @see https://tailwindcss.com/docs/will-change
			*/
			"will-change": [{ "will-change": [
				"auto",
				"scroll",
				"contents",
				"transform",
				isArbitraryVariable,
				isArbitraryValue
			] }],
			/**
			* Fill
			* @see https://tailwindcss.com/docs/fill
			*/
			fill: [{ fill: ["none", ...scaleColor()] }],
			/**
			* Stroke Width
			* @see https://tailwindcss.com/docs/stroke-width
			*/
			"stroke-w": [{ stroke: [
				isNumber,
				isArbitraryVariableLength,
				isArbitraryLength,
				isArbitraryNumber
			] }],
			/**
			* Stroke
			* @see https://tailwindcss.com/docs/stroke
			*/
			stroke: [{ stroke: ["none", ...scaleColor()] }],
			/**
			* Forced Color Adjust
			* @see https://tailwindcss.com/docs/forced-color-adjust
			*/
			"forced-color-adjust": [{ "forced-color-adjust": ["auto", "none"] }]
		},
		conflictingClassGroups: {
			"container-named": ["container-type"],
			overflow: ["overflow-x", "overflow-y"],
			overscroll: ["overscroll-x", "overscroll-y"],
			inset: [
				"inset-x",
				"inset-y",
				"inset-bs",
				"inset-be",
				"start",
				"end",
				"top",
				"right",
				"bottom",
				"left"
			],
			"inset-x": ["right", "left"],
			"inset-y": ["top", "bottom"],
			flex: [
				"basis",
				"grow",
				"shrink"
			],
			gap: ["gap-x", "gap-y"],
			p: [
				"px",
				"py",
				"ps",
				"pe",
				"pbs",
				"pbe",
				"pt",
				"pr",
				"pb",
				"pl"
			],
			px: ["pr", "pl"],
			py: ["pt", "pb"],
			m: [
				"mx",
				"my",
				"ms",
				"me",
				"mbs",
				"mbe",
				"mt",
				"mr",
				"mb",
				"ml"
			],
			mx: ["mr", "ml"],
			my: ["mt", "mb"],
			size: ["w", "h"],
			"font-size": ["leading"],
			"fvn-normal": [
				"fvn-ordinal",
				"fvn-slashed-zero",
				"fvn-figure",
				"fvn-spacing",
				"fvn-fraction"
			],
			"fvn-ordinal": ["fvn-normal"],
			"fvn-slashed-zero": ["fvn-normal"],
			"fvn-figure": ["fvn-normal"],
			"fvn-spacing": ["fvn-normal"],
			"fvn-fraction": ["fvn-normal"],
			"line-clamp": ["display", "overflow"],
			rounded: [
				"rounded-s",
				"rounded-e",
				"rounded-t",
				"rounded-r",
				"rounded-b",
				"rounded-l",
				"rounded-ss",
				"rounded-se",
				"rounded-ee",
				"rounded-es",
				"rounded-tl",
				"rounded-tr",
				"rounded-br",
				"rounded-bl"
			],
			"rounded-s": ["rounded-ss", "rounded-es"],
			"rounded-e": ["rounded-se", "rounded-ee"],
			"rounded-t": ["rounded-tl", "rounded-tr"],
			"rounded-r": ["rounded-tr", "rounded-br"],
			"rounded-b": ["rounded-br", "rounded-bl"],
			"rounded-l": ["rounded-tl", "rounded-bl"],
			"border-spacing": ["border-spacing-x", "border-spacing-y"],
			"border-w": [
				"border-w-x",
				"border-w-y",
				"border-w-s",
				"border-w-e",
				"border-w-bs",
				"border-w-be",
				"border-w-t",
				"border-w-r",
				"border-w-b",
				"border-w-l"
			],
			"border-w-x": ["border-w-r", "border-w-l"],
			"border-w-y": ["border-w-t", "border-w-b"],
			"border-color": [
				"border-color-x",
				"border-color-y",
				"border-color-s",
				"border-color-e",
				"border-color-bs",
				"border-color-be",
				"border-color-t",
				"border-color-r",
				"border-color-b",
				"border-color-l"
			],
			"border-color-x": ["border-color-r", "border-color-l"],
			"border-color-y": ["border-color-t", "border-color-b"],
			translate: [
				"translate-x",
				"translate-y",
				"translate-none"
			],
			"translate-none": [
				"translate",
				"translate-x",
				"translate-y",
				"translate-z"
			],
			"scroll-m": [
				"scroll-mx",
				"scroll-my",
				"scroll-ms",
				"scroll-me",
				"scroll-mbs",
				"scroll-mbe",
				"scroll-mt",
				"scroll-mr",
				"scroll-mb",
				"scroll-ml"
			],
			"scroll-mx": ["scroll-mr", "scroll-ml"],
			"scroll-my": ["scroll-mt", "scroll-mb"],
			"scroll-p": [
				"scroll-px",
				"scroll-py",
				"scroll-ps",
				"scroll-pe",
				"scroll-pbs",
				"scroll-pbe",
				"scroll-pt",
				"scroll-pr",
				"scroll-pb",
				"scroll-pl"
			],
			"scroll-px": ["scroll-pr", "scroll-pl"],
			"scroll-py": ["scroll-pt", "scroll-pb"],
			touch: [
				"touch-x",
				"touch-y",
				"touch-pz"
			],
			"touch-x": ["touch"],
			"touch-y": ["touch"],
			"touch-pz": ["touch"]
		},
		conflictingClassGroupModifiers: { "font-size": ["leading"] },
		postfixLookupClassGroups: ["container-type"],
		orderSensitiveModifiers: [
			"*",
			"**",
			"after",
			"backdrop",
			"before",
			"details-content",
			"file",
			"first-letter",
			"first-line",
			"marker",
			"placeholder",
			"selection"
		]
	};
};
/**
* @param baseConfig Config where other config will be merged into. This object will be mutated.
* @param configExtension Partial config to merge into the `baseConfig`.
*/
var mergeConfigs = (baseConfig, { cacheSize, prefix, experimentalParseClassName, extend = {}, override = {} }) => {
	overrideProperty(baseConfig, "cacheSize", cacheSize);
	overrideProperty(baseConfig, "prefix", prefix);
	overrideProperty(baseConfig, "experimentalParseClassName", experimentalParseClassName);
	overrideConfigProperties(baseConfig.theme, override.theme);
	overrideConfigProperties(baseConfig.classGroups, override.classGroups);
	overrideConfigProperties(baseConfig.conflictingClassGroups, override.conflictingClassGroups);
	overrideConfigProperties(baseConfig.conflictingClassGroupModifiers, override.conflictingClassGroupModifiers);
	overrideProperty(baseConfig, "postfixLookupClassGroups", override.postfixLookupClassGroups);
	overrideProperty(baseConfig, "orderSensitiveModifiers", override.orderSensitiveModifiers);
	mergeConfigProperties(baseConfig.theme, extend.theme);
	mergeConfigProperties(baseConfig.classGroups, extend.classGroups);
	mergeConfigProperties(baseConfig.conflictingClassGroups, extend.conflictingClassGroups);
	mergeConfigProperties(baseConfig.conflictingClassGroupModifiers, extend.conflictingClassGroupModifiers);
	mergeArrayProperties(baseConfig, extend, "postfixLookupClassGroups");
	mergeArrayProperties(baseConfig, extend, "orderSensitiveModifiers");
	return baseConfig;
};
var overrideProperty = (baseObject, overrideKey, overrideValue) => {
	if (overrideValue !== void 0) baseObject[overrideKey] = overrideValue;
};
var overrideConfigProperties = (baseObject, overrideObject) => {
	if (overrideObject) for (const key in overrideObject) overrideProperty(baseObject, key, overrideObject[key]);
};
var mergeConfigProperties = (baseObject, mergeObject) => {
	if (mergeObject) for (const key in mergeObject) mergeArrayProperties(baseObject, mergeObject, key);
};
var mergeArrayProperties = (baseObject, mergeObject, key) => {
	const mergeValue = mergeObject[key];
	if (mergeValue !== void 0) baseObject[key] = baseObject[key] ? baseObject[key].concat(mergeValue) : mergeValue;
};
var extendTailwindMerge = (configExtension, ...createConfig) => typeof configExtension === "function" ? createTailwindMerge(getDefaultConfig, configExtension, ...createConfig) : createTailwindMerge(() => mergeConfigs(getDefaultConfig(), configExtension), ...createConfig);
var twMerge = /*#__PURE__*/ createTailwindMerge(getDefaultConfig);
//#endregion
export { createTailwindMerge, extendTailwindMerge, fromTheme, getDefaultConfig, mergeConfigs, twJoin, twMerge, validators };

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGFpbHdpbmQtbWVyZ2UuanMiLCJuYW1lcyI6W10sInNvdXJjZXMiOlsiLi4vLi4vdGFpbHdpbmQtbWVyZ2UvZGlzdC9idW5kbGUtbWpzLm1qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIENvbmNhdGVuYXRlcyB0d28gYXJyYXlzIGZhc3RlciB0aGFuIHRoZSBhcnJheSBzcHJlYWQgb3BlcmF0b3IuXG4gKi9cbmNvbnN0IGNvbmNhdEFycmF5cyA9IChhcnJheTEsIGFycmF5MikgPT4ge1xuICAvLyBQcmUtYWxsb2NhdGUgZm9yIGJldHRlciBWOCBvcHRpbWl6YXRpb25cbiAgY29uc3QgY29tYmluZWRBcnJheSA9IG5ldyBBcnJheShhcnJheTEubGVuZ3RoICsgYXJyYXkyLmxlbmd0aCk7XG4gIGZvciAobGV0IGkgPSAwOyBpIDwgYXJyYXkxLmxlbmd0aDsgaSsrKSB7XG4gICAgY29tYmluZWRBcnJheVtpXSA9IGFycmF5MVtpXTtcbiAgfVxuICBmb3IgKGxldCBpID0gMDsgaSA8IGFycmF5Mi5sZW5ndGg7IGkrKykge1xuICAgIGNvbWJpbmVkQXJyYXlbYXJyYXkxLmxlbmd0aCArIGldID0gYXJyYXkyW2ldO1xuICB9XG4gIHJldHVybiBjb21iaW5lZEFycmF5O1xufTtcblxuLy8gRmFjdG9yeSBmdW5jdGlvbiBlbnN1cmVzIGNvbnNpc3RlbnQgb2JqZWN0IHNoYXBlc1xuY29uc3QgY3JlYXRlQ2xhc3NWYWxpZGF0b3JPYmplY3QgPSAoY2xhc3NHcm91cElkLCB2YWxpZGF0b3IpID0+ICh7XG4gIGNsYXNzR3JvdXBJZCxcbiAgdmFsaWRhdG9yXG59KTtcbi8vIEZhY3RvcnkgZW5zdXJlcyBjb25zaXN0ZW50IENsYXNzUGFydE9iamVjdCBzaGFwZVxuY29uc3QgY3JlYXRlQ2xhc3NQYXJ0T2JqZWN0ID0gKG5leHRQYXJ0ID0gbmV3IE1hcCgpLCB2YWxpZGF0b3JzID0gbnVsbCwgY2xhc3NHcm91cElkKSA9PiAoe1xuICBuZXh0UGFydCxcbiAgdmFsaWRhdG9ycyxcbiAgY2xhc3NHcm91cElkXG59KTtcbmNvbnN0IENMQVNTX1BBUlRfU0VQQVJBVE9SID0gJy0nO1xuY29uc3QgRU1QVFlfQ09ORkxJQ1RTID0gW107XG4vLyBJIHVzZSB0d28gZG90cyBoZXJlIGJlY2F1c2Ugb25lIGRvdCBpcyB1c2VkIGFzIHByZWZpeCBmb3IgY2xhc3MgZ3JvdXBzIGluIHBsdWdpbnNcbmNvbnN0IEFSQklUUkFSWV9QUk9QRVJUWV9QUkVGSVggPSAnYXJiaXRyYXJ5Li4nO1xuY29uc3QgY3JlYXRlQ2xhc3NHcm91cFV0aWxzID0gY29uZmlnID0+IHtcbiAgY29uc3QgY2xhc3NNYXAgPSBjcmVhdGVDbGFzc01hcChjb25maWcpO1xuICBjb25zdCB7XG4gICAgY29uZmxpY3RpbmdDbGFzc0dyb3VwcyxcbiAgICBjb25mbGljdGluZ0NsYXNzR3JvdXBNb2RpZmllcnNcbiAgfSA9IGNvbmZpZztcbiAgY29uc3QgZ2V0Q2xhc3NHcm91cElkID0gY2xhc3NOYW1lID0+IHtcbiAgICBpZiAoY2xhc3NOYW1lLnN0YXJ0c1dpdGgoJ1snKSAmJiBjbGFzc05hbWUuZW5kc1dpdGgoJ10nKSkge1xuICAgICAgcmV0dXJuIGdldEdyb3VwSWRGb3JBcmJpdHJhcnlQcm9wZXJ0eShjbGFzc05hbWUpO1xuICAgIH1cbiAgICBjb25zdCBjbGFzc1BhcnRzID0gY2xhc3NOYW1lLnNwbGl0KENMQVNTX1BBUlRfU0VQQVJBVE9SKTtcbiAgICAvLyBDbGFzc2VzIGxpa2UgYC1pbnNldC0xYCBwcm9kdWNlIGFuIGVtcHR5IHN0cmluZyBhcyBmaXJzdCBjbGFzc1BhcnQuIFdlIGFzc3VtZSB0aGF0IGNsYXNzZXMgZm9yIG5lZ2F0aXZlIHZhbHVlcyBhcmUgdXNlZCBjb3JyZWN0bHkgYW5kIHNraXAgaXQuXG4gICAgY29uc3Qgc3RhcnRJbmRleCA9IGNsYXNzUGFydHNbMF0gPT09ICcnICYmIGNsYXNzUGFydHMubGVuZ3RoID4gMSA/IDEgOiAwO1xuICAgIHJldHVybiBnZXRHcm91cFJlY3Vyc2l2ZShjbGFzc1BhcnRzLCBzdGFydEluZGV4LCBjbGFzc01hcCk7XG4gIH07XG4gIGNvbnN0IGdldENvbmZsaWN0aW5nQ2xhc3NHcm91cElkcyA9IChjbGFzc0dyb3VwSWQsIGhhc1Bvc3RmaXhNb2RpZmllcikgPT4ge1xuICAgIGlmIChoYXNQb3N0Zml4TW9kaWZpZXIpIHtcbiAgICAgIGNvbnN0IG1vZGlmaWVyQ29uZmxpY3RzID0gY29uZmxpY3RpbmdDbGFzc0dyb3VwTW9kaWZpZXJzW2NsYXNzR3JvdXBJZF07XG4gICAgICBjb25zdCBiYXNlQ29uZmxpY3RzID0gY29uZmxpY3RpbmdDbGFzc0dyb3Vwc1tjbGFzc0dyb3VwSWRdO1xuICAgICAgaWYgKG1vZGlmaWVyQ29uZmxpY3RzKSB7XG4gICAgICAgIGlmIChiYXNlQ29uZmxpY3RzKSB7XG4gICAgICAgICAgLy8gTWVyZ2UgYmFzZSBjb25mbGljdHMgd2l0aCBtb2RpZmllciBjb25mbGljdHNcbiAgICAgICAgICByZXR1cm4gY29uY2F0QXJyYXlzKGJhc2VDb25mbGljdHMsIG1vZGlmaWVyQ29uZmxpY3RzKTtcbiAgICAgICAgfVxuICAgICAgICAvLyBPbmx5IG1vZGlmaWVyIGNvbmZsaWN0c1xuICAgICAgICByZXR1cm4gbW9kaWZpZXJDb25mbGljdHM7XG4gICAgICB9XG4gICAgICAvLyBGYWxsIGJhY2sgdG8gd2l0aG91dCBwb3N0Zml4IGlmIG5vIG1vZGlmaWVyIGNvbmZsaWN0c1xuICAgICAgcmV0dXJuIGJhc2VDb25mbGljdHMgfHwgRU1QVFlfQ09ORkxJQ1RTO1xuICAgIH1cbiAgICByZXR1cm4gY29uZmxpY3RpbmdDbGFzc0dyb3Vwc1tjbGFzc0dyb3VwSWRdIHx8IEVNUFRZX0NPTkZMSUNUUztcbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBnZXRDbGFzc0dyb3VwSWQsXG4gICAgZ2V0Q29uZmxpY3RpbmdDbGFzc0dyb3VwSWRzXG4gIH07XG59O1xuY29uc3QgZ2V0R3JvdXBSZWN1cnNpdmUgPSAoY2xhc3NQYXJ0cywgc3RhcnRJbmRleCwgY2xhc3NQYXJ0T2JqZWN0KSA9PiB7XG4gIGNvbnN0IGNsYXNzUGF0aHNMZW5ndGggPSBjbGFzc1BhcnRzLmxlbmd0aCAtIHN0YXJ0SW5kZXg7XG4gIGlmIChjbGFzc1BhdGhzTGVuZ3RoID09PSAwKSB7XG4gICAgcmV0dXJuIGNsYXNzUGFydE9iamVjdC5jbGFzc0dyb3VwSWQ7XG4gIH1cbiAgY29uc3QgY3VycmVudENsYXNzUGFydCA9IGNsYXNzUGFydHNbc3RhcnRJbmRleF07XG4gIGNvbnN0IG5leHRDbGFzc1BhcnRPYmplY3QgPSBjbGFzc1BhcnRPYmplY3QubmV4dFBhcnQuZ2V0KGN1cnJlbnRDbGFzc1BhcnQpO1xuICBpZiAobmV4dENsYXNzUGFydE9iamVjdCkge1xuICAgIGNvbnN0IHJlc3VsdCA9IGdldEdyb3VwUmVjdXJzaXZlKGNsYXNzUGFydHMsIHN0YXJ0SW5kZXggKyAxLCBuZXh0Q2xhc3NQYXJ0T2JqZWN0KTtcbiAgICBpZiAocmVzdWx0KSByZXR1cm4gcmVzdWx0O1xuICB9XG4gIGNvbnN0IHZhbGlkYXRvcnMgPSBjbGFzc1BhcnRPYmplY3QudmFsaWRhdG9ycztcbiAgaWYgKHZhbGlkYXRvcnMgPT09IG51bGwpIHtcbiAgICByZXR1cm4gdW5kZWZpbmVkO1xuICB9XG4gIC8vIEJ1aWxkIGNsYXNzUmVzdCBzdHJpbmcgZWZmaWNpZW50bHkgYnkgam9pbmluZyBmcm9tIHN0YXJ0SW5kZXggb253YXJkc1xuICBjb25zdCBjbGFzc1Jlc3QgPSBzdGFydEluZGV4ID09PSAwID8gY2xhc3NQYXJ0cy5qb2luKENMQVNTX1BBUlRfU0VQQVJBVE9SKSA6IGNsYXNzUGFydHMuc2xpY2Uoc3RhcnRJbmRleCkuam9pbihDTEFTU19QQVJUX1NFUEFSQVRPUik7XG4gIGNvbnN0IHZhbGlkYXRvcnNMZW5ndGggPSB2YWxpZGF0b3JzLmxlbmd0aDtcbiAgZm9yIChsZXQgaSA9IDA7IGkgPCB2YWxpZGF0b3JzTGVuZ3RoOyBpKyspIHtcbiAgICBjb25zdCB2YWxpZGF0b3JPYmogPSB2YWxpZGF0b3JzW2ldO1xuICAgIGlmICh2YWxpZGF0b3JPYmoudmFsaWRhdG9yKGNsYXNzUmVzdCkpIHtcbiAgICAgIHJldHVybiB2YWxpZGF0b3JPYmouY2xhc3NHcm91cElkO1xuICAgIH1cbiAgfVxuICByZXR1cm4gdW5kZWZpbmVkO1xufTtcbi8qKlxuICogR2V0IHRoZSBjbGFzcyBncm91cCBJRCBmb3IgYW4gYXJiaXRyYXJ5IHByb3BlcnR5LlxuICpcbiAqIEBwYXJhbSBjbGFzc05hbWUgLSBUaGUgY2xhc3MgbmFtZSB0byBnZXQgdGhlIGdyb3VwIElEIGZvci4gSXMgZXhwZWN0ZWQgdG8gYmUgc3RyaW5nIHN0YXJ0aW5nIHdpdGggYFtgIGFuZCBlbmRpbmcgd2l0aCBgXWAuXG4gKi9cbmNvbnN0IGdldEdyb3VwSWRGb3JBcmJpdHJhcnlQcm9wZXJ0eSA9IGNsYXNzTmFtZSA9PiBjbGFzc05hbWUuc2xpY2UoMSwgLTEpLmluZGV4T2YoJzonKSA9PT0gLTEgPyB1bmRlZmluZWQgOiAoKCkgPT4ge1xuICBjb25zdCBjb250ZW50ID0gY2xhc3NOYW1lLnNsaWNlKDEsIC0xKTtcbiAgY29uc3QgY29sb25JbmRleCA9IGNvbnRlbnQuaW5kZXhPZignOicpO1xuICBjb25zdCBwcm9wZXJ0eSA9IGNvbnRlbnQuc2xpY2UoMCwgY29sb25JbmRleCk7XG4gIHJldHVybiBwcm9wZXJ0eSA/IEFSQklUUkFSWV9QUk9QRVJUWV9QUkVGSVggKyBwcm9wZXJ0eSA6IHVuZGVmaW5lZDtcbn0pKCk7XG4vKipcbiAqIEV4cG9ydGVkIGZvciB0ZXN0aW5nIG9ubHlcbiAqL1xuY29uc3QgY3JlYXRlQ2xhc3NNYXAgPSBjb25maWcgPT4ge1xuICBjb25zdCB7XG4gICAgdGhlbWUsXG4gICAgY2xhc3NHcm91cHNcbiAgfSA9IGNvbmZpZztcbiAgcmV0dXJuIHByb2Nlc3NDbGFzc0dyb3VwcyhjbGFzc0dyb3VwcywgdGhlbWUpO1xufTtcbi8vIFNwbGl0IGludG8gc2VwYXJhdGUgZnVuY3Rpb25zIHRvIG1haW50YWluIG1vbm9tb3JwaGljIGNhbGwgc2l0ZXNcbmNvbnN0IHByb2Nlc3NDbGFzc0dyb3VwcyA9IChjbGFzc0dyb3VwcywgdGhlbWUpID0+IHtcbiAgY29uc3QgY2xhc3NNYXAgPSBjcmVhdGVDbGFzc1BhcnRPYmplY3QoKTtcbiAgZm9yIChjb25zdCBjbGFzc0dyb3VwSWQgaW4gY2xhc3NHcm91cHMpIHtcbiAgICBjb25zdCBncm91cCA9IGNsYXNzR3JvdXBzW2NsYXNzR3JvdXBJZF07XG4gICAgcHJvY2Vzc0NsYXNzZXNSZWN1cnNpdmVseShncm91cCwgY2xhc3NNYXAsIGNsYXNzR3JvdXBJZCwgdGhlbWUpO1xuICB9XG4gIHJldHVybiBjbGFzc01hcDtcbn07XG5jb25zdCBwcm9jZXNzQ2xhc3Nlc1JlY3Vyc2l2ZWx5ID0gKGNsYXNzR3JvdXAsIGNsYXNzUGFydE9iamVjdCwgY2xhc3NHcm91cElkLCB0aGVtZSkgPT4ge1xuICBjb25zdCBsZW4gPSBjbGFzc0dyb3VwLmxlbmd0aDtcbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBsZW47IGkrKykge1xuICAgIGNvbnN0IGNsYXNzRGVmaW5pdGlvbiA9IGNsYXNzR3JvdXBbaV07XG4gICAgcHJvY2Vzc0NsYXNzRGVmaW5pdGlvbihjbGFzc0RlZmluaXRpb24sIGNsYXNzUGFydE9iamVjdCwgY2xhc3NHcm91cElkLCB0aGVtZSk7XG4gIH1cbn07XG4vLyBTcGxpdCBpbnRvIHNlcGFyYXRlIGZ1bmN0aW9ucyBmb3IgZWFjaCB0eXBlIHRvIG1haW50YWluIG1vbm9tb3JwaGljIGNhbGwgc2l0ZXNcbmNvbnN0IHByb2Nlc3NDbGFzc0RlZmluaXRpb24gPSAoY2xhc3NEZWZpbml0aW9uLCBjbGFzc1BhcnRPYmplY3QsIGNsYXNzR3JvdXBJZCwgdGhlbWUpID0+IHtcbiAgaWYgKHR5cGVvZiBjbGFzc0RlZmluaXRpb24gPT09ICdzdHJpbmcnKSB7XG4gICAgcHJvY2Vzc1N0cmluZ0RlZmluaXRpb24oY2xhc3NEZWZpbml0aW9uLCBjbGFzc1BhcnRPYmplY3QsIGNsYXNzR3JvdXBJZCk7XG4gICAgcmV0dXJuO1xuICB9XG4gIGlmICh0eXBlb2YgY2xhc3NEZWZpbml0aW9uID09PSAnZnVuY3Rpb24nKSB7XG4gICAgcHJvY2Vzc0Z1bmN0aW9uRGVmaW5pdGlvbihjbGFzc0RlZmluaXRpb24sIGNsYXNzUGFydE9iamVjdCwgY2xhc3NHcm91cElkLCB0aGVtZSk7XG4gICAgcmV0dXJuO1xuICB9XG4gIHByb2Nlc3NPYmplY3REZWZpbml0aW9uKGNsYXNzRGVmaW5pdGlvbiwgY2xhc3NQYXJ0T2JqZWN0LCBjbGFzc0dyb3VwSWQsIHRoZW1lKTtcbn07XG5jb25zdCBwcm9jZXNzU3RyaW5nRGVmaW5pdGlvbiA9IChjbGFzc0RlZmluaXRpb24sIGNsYXNzUGFydE9iamVjdCwgY2xhc3NHcm91cElkKSA9PiB7XG4gIGNvbnN0IGNsYXNzUGFydE9iamVjdFRvRWRpdCA9IGNsYXNzRGVmaW5pdGlvbiA9PT0gJycgPyBjbGFzc1BhcnRPYmplY3QgOiBnZXRQYXJ0KGNsYXNzUGFydE9iamVjdCwgY2xhc3NEZWZpbml0aW9uKTtcbiAgY2xhc3NQYXJ0T2JqZWN0VG9FZGl0LmNsYXNzR3JvdXBJZCA9IGNsYXNzR3JvdXBJZDtcbn07XG5jb25zdCBwcm9jZXNzRnVuY3Rpb25EZWZpbml0aW9uID0gKGNsYXNzRGVmaW5pdGlvbiwgY2xhc3NQYXJ0T2JqZWN0LCBjbGFzc0dyb3VwSWQsIHRoZW1lKSA9PiB7XG4gIGlmIChpc1RoZW1lR2V0dGVyKGNsYXNzRGVmaW5pdGlvbikpIHtcbiAgICBwcm9jZXNzQ2xhc3Nlc1JlY3Vyc2l2ZWx5KGNsYXNzRGVmaW5pdGlvbih0aGVtZSksIGNsYXNzUGFydE9iamVjdCwgY2xhc3NHcm91cElkLCB0aGVtZSk7XG4gICAgcmV0dXJuO1xuICB9XG4gIGlmIChjbGFzc1BhcnRPYmplY3QudmFsaWRhdG9ycyA9PT0gbnVsbCkge1xuICAgIGNsYXNzUGFydE9iamVjdC52YWxpZGF0b3JzID0gW107XG4gIH1cbiAgY2xhc3NQYXJ0T2JqZWN0LnZhbGlkYXRvcnMucHVzaChjcmVhdGVDbGFzc1ZhbGlkYXRvck9iamVjdChjbGFzc0dyb3VwSWQsIGNsYXNzRGVmaW5pdGlvbikpO1xufTtcbmNvbnN0IHByb2Nlc3NPYmplY3REZWZpbml0aW9uID0gKGNsYXNzRGVmaW5pdGlvbiwgY2xhc3NQYXJ0T2JqZWN0LCBjbGFzc0dyb3VwSWQsIHRoZW1lKSA9PiB7XG4gIGNvbnN0IGVudHJpZXMgPSBPYmplY3QuZW50cmllcyhjbGFzc0RlZmluaXRpb24pO1xuICBjb25zdCBsZW4gPSBlbnRyaWVzLmxlbmd0aDtcbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBsZW47IGkrKykge1xuICAgIGNvbnN0IFtrZXksIHZhbHVlXSA9IGVudHJpZXNbaV07XG4gICAgcHJvY2Vzc0NsYXNzZXNSZWN1cnNpdmVseSh2YWx1ZSwgZ2V0UGFydChjbGFzc1BhcnRPYmplY3QsIGtleSksIGNsYXNzR3JvdXBJZCwgdGhlbWUpO1xuICB9XG59O1xuY29uc3QgZ2V0UGFydCA9IChjbGFzc1BhcnRPYmplY3QsIHBhdGgpID0+IHtcbiAgbGV0IGN1cnJlbnQgPSBjbGFzc1BhcnRPYmplY3Q7XG4gIGNvbnN0IHBhcnRzID0gcGF0aC5zcGxpdChDTEFTU19QQVJUX1NFUEFSQVRPUik7XG4gIGNvbnN0IGxlbiA9IHBhcnRzLmxlbmd0aDtcbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBsZW47IGkrKykge1xuICAgIGNvbnN0IHBhcnQgPSBwYXJ0c1tpXTtcbiAgICBsZXQgbmV4dCA9IGN1cnJlbnQubmV4dFBhcnQuZ2V0KHBhcnQpO1xuICAgIGlmICghbmV4dCkge1xuICAgICAgbmV4dCA9IGNyZWF0ZUNsYXNzUGFydE9iamVjdCgpO1xuICAgICAgY3VycmVudC5uZXh0UGFydC5zZXQocGFydCwgbmV4dCk7XG4gICAgfVxuICAgIGN1cnJlbnQgPSBuZXh0O1xuICB9XG4gIHJldHVybiBjdXJyZW50O1xufTtcbi8vIFR5cGUgZ3VhcmQgbWFpbnRhaW5zIG1vbm9tb3JwaGljIGNoZWNrXG5jb25zdCBpc1RoZW1lR2V0dGVyID0gZnVuYyA9PiAnaXNUaGVtZUdldHRlcicgaW4gZnVuYyAmJiBmdW5jLmlzVGhlbWVHZXR0ZXIgPT09IHRydWU7XG5cbi8vIExSVSBjYWNoZSBpbXBsZW1lbnRhdGlvbiB1c2luZyBwbGFpbiBvYmplY3RzIGZvciBzaW1wbGljaXR5XG5jb25zdCBjcmVhdGVMcnVDYWNoZSA9IG1heENhY2hlU2l6ZSA9PiB7XG4gIGlmIChtYXhDYWNoZVNpemUgPCAxKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGdldDogKCkgPT4gdW5kZWZpbmVkLFxuICAgICAgc2V0OiAoKSA9PiB7fVxuICAgIH07XG4gIH1cbiAgbGV0IGNhY2hlU2l6ZSA9IDA7XG4gIGxldCBjYWNoZSA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gIGxldCBwcmV2aW91c0NhY2hlID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiAgY29uc3QgdXBkYXRlID0gKGtleSwgdmFsdWUpID0+IHtcbiAgICBjYWNoZVtrZXldID0gdmFsdWU7XG4gICAgY2FjaGVTaXplKys7XG4gICAgaWYgKGNhY2hlU2l6ZSA+IG1heENhY2hlU2l6ZSkge1xuICAgICAgY2FjaGVTaXplID0gMDtcbiAgICAgIHByZXZpb3VzQ2FjaGUgPSBjYWNoZTtcbiAgICAgIGNhY2hlID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiAgICB9XG4gIH07XG4gIHJldHVybiB7XG4gICAgZ2V0KGtleSkge1xuICAgICAgbGV0IHZhbHVlID0gY2FjaGVba2V5XTtcbiAgICAgIGlmICh2YWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIHJldHVybiB2YWx1ZTtcbiAgICAgIH1cbiAgICAgIGlmICgodmFsdWUgPSBwcmV2aW91c0NhY2hlW2tleV0pICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgdXBkYXRlKGtleSwgdmFsdWUpO1xuICAgICAgICByZXR1cm4gdmFsdWU7XG4gICAgICB9XG4gICAgfSxcbiAgICBzZXQoa2V5LCB2YWx1ZSkge1xuICAgICAgaWYgKGtleSBpbiBjYWNoZSkge1xuICAgICAgICBjYWNoZVtrZXldID0gdmFsdWU7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB1cGRhdGUoa2V5LCB2YWx1ZSk7XG4gICAgICB9XG4gICAgfVxuICB9O1xufTtcbmNvbnN0IElNUE9SVEFOVF9NT0RJRklFUiA9ICchJztcbmNvbnN0IE1PRElGSUVSX1NFUEFSQVRPUiA9ICc6JztcbmNvbnN0IEVNUFRZX01PRElGSUVSUyA9IFtdO1xuLy8gUHJlLWFsbG9jYXRlZCByZXN1bHQgb2JqZWN0IHNoYXBlIGZvciBjb25zaXN0ZW5jeVxuY29uc3QgY3JlYXRlUmVzdWx0T2JqZWN0ID0gKG1vZGlmaWVycywgaGFzSW1wb3J0YW50TW9kaWZpZXIsIGJhc2VDbGFzc05hbWUsIG1heWJlUG9zdGZpeE1vZGlmaWVyUG9zaXRpb24sIGlzRXh0ZXJuYWwpID0+ICh7XG4gIG1vZGlmaWVycyxcbiAgaGFzSW1wb3J0YW50TW9kaWZpZXIsXG4gIGJhc2VDbGFzc05hbWUsXG4gIG1heWJlUG9zdGZpeE1vZGlmaWVyUG9zaXRpb24sXG4gIGlzRXh0ZXJuYWxcbn0pO1xuY29uc3QgY3JlYXRlUGFyc2VDbGFzc05hbWUgPSBjb25maWcgPT4ge1xuICBjb25zdCB7XG4gICAgcHJlZml4LFxuICAgIGV4cGVyaW1lbnRhbFBhcnNlQ2xhc3NOYW1lXG4gIH0gPSBjb25maWc7XG4gIC8qKlxuICAgKiBQYXJzZSBjbGFzcyBuYW1lIGludG8gcGFydHMuXG4gICAqXG4gICAqIEluc3BpcmVkIGJ5IGBzcGxpdEF0VG9wTGV2ZWxPbmx5YCB1c2VkIGluIFRhaWx3aW5kIENTU1xuICAgKiBAc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS90YWlsd2luZGxhYnMvdGFpbHdpbmRjc3MvYmxvYi92My4yLjIvc3JjL3V0aWwvc3BsaXRBdFRvcExldmVsT25seS5qc1xuICAgKi9cbiAgbGV0IHBhcnNlQ2xhc3NOYW1lID0gY2xhc3NOYW1lID0+IHtcbiAgICAvLyBVc2Ugc2ltcGxlIGFycmF5IHdpdGggcHVzaCBmb3IgYmV0dGVyIHBlcmZvcm1hbmNlXG4gICAgY29uc3QgbW9kaWZpZXJzID0gW107XG4gICAgbGV0IGJyYWNrZXREZXB0aCA9IDA7XG4gICAgbGV0IHBhcmVuRGVwdGggPSAwO1xuICAgIGxldCBtb2RpZmllclN0YXJ0ID0gMDtcbiAgICBsZXQgcG9zdGZpeE1vZGlmaWVyUG9zaXRpb247XG4gICAgY29uc3QgbGVuID0gY2xhc3NOYW1lLmxlbmd0aDtcbiAgICBmb3IgKGxldCBpbmRleCA9IDA7IGluZGV4IDwgbGVuOyBpbmRleCsrKSB7XG4gICAgICBjb25zdCBjdXJyZW50Q2hhcmFjdGVyID0gY2xhc3NOYW1lW2luZGV4XTtcbiAgICAgIGlmIChicmFja2V0RGVwdGggPT09IDAgJiYgcGFyZW5EZXB0aCA9PT0gMCkge1xuICAgICAgICBpZiAoY3VycmVudENoYXJhY3RlciA9PT0gTU9ESUZJRVJfU0VQQVJBVE9SKSB7XG4gICAgICAgICAgbW9kaWZpZXJzLnB1c2goY2xhc3NOYW1lLnNsaWNlKG1vZGlmaWVyU3RhcnQsIGluZGV4KSk7XG4gICAgICAgICAgbW9kaWZpZXJTdGFydCA9IGluZGV4ICsgMTtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoY3VycmVudENoYXJhY3RlciA9PT0gJy8nKSB7XG4gICAgICAgICAgcG9zdGZpeE1vZGlmaWVyUG9zaXRpb24gPSBpbmRleDtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgaWYgKGN1cnJlbnRDaGFyYWN0ZXIgPT09ICdbJykgYnJhY2tldERlcHRoKys7ZWxzZSBpZiAoY3VycmVudENoYXJhY3RlciA9PT0gJ10nKSBicmFja2V0RGVwdGgtLTtlbHNlIGlmIChjdXJyZW50Q2hhcmFjdGVyID09PSAnKCcpIHBhcmVuRGVwdGgrKztlbHNlIGlmIChjdXJyZW50Q2hhcmFjdGVyID09PSAnKScpIHBhcmVuRGVwdGgtLTtcbiAgICB9XG4gICAgY29uc3QgYmFzZUNsYXNzTmFtZVdpdGhJbXBvcnRhbnRNb2RpZmllciA9IG1vZGlmaWVycy5sZW5ndGggPT09IDAgPyBjbGFzc05hbWUgOiBjbGFzc05hbWUuc2xpY2UobW9kaWZpZXJTdGFydCk7XG4gICAgLy8gSW5saW5lIGltcG9ydGFudCBtb2RpZmllciBjaGVja1xuICAgIGxldCBiYXNlQ2xhc3NOYW1lID0gYmFzZUNsYXNzTmFtZVdpdGhJbXBvcnRhbnRNb2RpZmllcjtcbiAgICBsZXQgaGFzSW1wb3J0YW50TW9kaWZpZXIgPSBmYWxzZTtcbiAgICBpZiAoYmFzZUNsYXNzTmFtZVdpdGhJbXBvcnRhbnRNb2RpZmllci5lbmRzV2l0aChJTVBPUlRBTlRfTU9ESUZJRVIpKSB7XG4gICAgICBiYXNlQ2xhc3NOYW1lID0gYmFzZUNsYXNzTmFtZVdpdGhJbXBvcnRhbnRNb2RpZmllci5zbGljZSgwLCAtMSk7XG4gICAgICBoYXNJbXBvcnRhbnRNb2RpZmllciA9IHRydWU7XG4gICAgfSBlbHNlIGlmIChcbiAgICAvKipcbiAgICAgKiBJbiBUYWlsd2luZCBDU1MgdjMgdGhlIGltcG9ydGFudCBtb2RpZmllciB3YXMgYXQgdGhlIHN0YXJ0IG9mIHRoZSBiYXNlIGNsYXNzIG5hbWUuIFRoaXMgaXMgc3RpbGwgc3VwcG9ydGVkIGZvciBsZWdhY3kgcmVhc29ucy5cbiAgICAgKiBAc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS9kY2FzdGlsL3RhaWx3aW5kLW1lcmdlL2lzc3Vlcy81MTMjaXNzdWVjb21tZW50LTI2MTQwMjk4NjRcbiAgICAgKi9cbiAgICBiYXNlQ2xhc3NOYW1lV2l0aEltcG9ydGFudE1vZGlmaWVyLnN0YXJ0c1dpdGgoSU1QT1JUQU5UX01PRElGSUVSKSkge1xuICAgICAgYmFzZUNsYXNzTmFtZSA9IGJhc2VDbGFzc05hbWVXaXRoSW1wb3J0YW50TW9kaWZpZXIuc2xpY2UoMSk7XG4gICAgICBoYXNJbXBvcnRhbnRNb2RpZmllciA9IHRydWU7XG4gICAgfVxuICAgIGNvbnN0IG1heWJlUG9zdGZpeE1vZGlmaWVyUG9zaXRpb24gPSBwb3N0Zml4TW9kaWZpZXJQb3NpdGlvbiAmJiBwb3N0Zml4TW9kaWZpZXJQb3NpdGlvbiA+IG1vZGlmaWVyU3RhcnQgPyBwb3N0Zml4TW9kaWZpZXJQb3NpdGlvbiAtIG1vZGlmaWVyU3RhcnQgOiB1bmRlZmluZWQ7XG4gICAgcmV0dXJuIGNyZWF0ZVJlc3VsdE9iamVjdChtb2RpZmllcnMsIGhhc0ltcG9ydGFudE1vZGlmaWVyLCBiYXNlQ2xhc3NOYW1lLCBtYXliZVBvc3RmaXhNb2RpZmllclBvc2l0aW9uKTtcbiAgfTtcbiAgaWYgKHByZWZpeCkge1xuICAgIGNvbnN0IGZ1bGxQcmVmaXggPSBwcmVmaXggKyBNT0RJRklFUl9TRVBBUkFUT1I7XG4gICAgY29uc3QgcGFyc2VDbGFzc05hbWVPcmlnaW5hbCA9IHBhcnNlQ2xhc3NOYW1lO1xuICAgIHBhcnNlQ2xhc3NOYW1lID0gY2xhc3NOYW1lID0+IGNsYXNzTmFtZS5zdGFydHNXaXRoKGZ1bGxQcmVmaXgpID8gcGFyc2VDbGFzc05hbWVPcmlnaW5hbChjbGFzc05hbWUuc2xpY2UoZnVsbFByZWZpeC5sZW5ndGgpKSA6IGNyZWF0ZVJlc3VsdE9iamVjdChFTVBUWV9NT0RJRklFUlMsIGZhbHNlLCBjbGFzc05hbWUsIHVuZGVmaW5lZCwgdHJ1ZSk7XG4gIH1cbiAgaWYgKGV4cGVyaW1lbnRhbFBhcnNlQ2xhc3NOYW1lKSB7XG4gICAgY29uc3QgcGFyc2VDbGFzc05hbWVPcmlnaW5hbCA9IHBhcnNlQ2xhc3NOYW1lO1xuICAgIHBhcnNlQ2xhc3NOYW1lID0gY2xhc3NOYW1lID0+IGV4cGVyaW1lbnRhbFBhcnNlQ2xhc3NOYW1lKHtcbiAgICAgIGNsYXNzTmFtZSxcbiAgICAgIHBhcnNlQ2xhc3NOYW1lOiBwYXJzZUNsYXNzTmFtZU9yaWdpbmFsXG4gICAgfSk7XG4gIH1cbiAgcmV0dXJuIHBhcnNlQ2xhc3NOYW1lO1xufTtcblxuLyoqXG4gKiBTb3J0cyBtb2RpZmllcnMgYWNjb3JkaW5nIHRvIGZvbGxvd2luZyBzY2hlbWE6XG4gKiAtIFByZWRlZmluZWQgbW9kaWZpZXJzIGFyZSBzb3J0ZWQgYWxwaGFiZXRpY2FsbHlcbiAqIC0gV2hlbiBhbiBhcmJpdHJhcnkgdmFyaWFudCBhcHBlYXJzLCBpdCBtdXN0IGJlIHByZXNlcnZlZCB3aGljaCBtb2RpZmllcnMgYXJlIGJlZm9yZSBhbmQgYWZ0ZXIgaXRcbiAqL1xuY29uc3QgY3JlYXRlU29ydE1vZGlmaWVycyA9IGNvbmZpZyA9PiB7XG4gIC8vIFByZS1jb21wdXRlIHdlaWdodHMgZm9yIGFsbCBrbm93biBtb2RpZmllcnMgZm9yIE8oMSkgY29tcGFyaXNvblxuICBjb25zdCBtb2RpZmllcldlaWdodHMgPSBuZXcgTWFwKCk7XG4gIC8vIEFzc2lnbiB3ZWlnaHRzIHRvIHNlbnNpdGl2ZSBtb2RpZmllcnMgKGhpZ2hlc3QgcHJpb3JpdHksIGJ1dCBwcmVzZXJ2ZSBvcmRlcilcbiAgY29uZmlnLm9yZGVyU2Vuc2l0aXZlTW9kaWZpZXJzLmZvckVhY2goKG1vZCwgaW5kZXgpID0+IHtcbiAgICBtb2RpZmllcldlaWdodHMuc2V0KG1vZCwgMTAwMDAwMCArIGluZGV4KTsgLy8gSGlnaCB3ZWlnaHRzIGZvciBzZW5zaXRpdmUgbW9kc1xuICB9KTtcbiAgcmV0dXJuIG1vZGlmaWVycyA9PiB7XG4gICAgY29uc3QgcmVzdWx0ID0gW107XG4gICAgbGV0IGN1cnJlbnRTZWdtZW50ID0gW107XG4gICAgLy8gUHJvY2VzcyBtb2RpZmllcnMgaW4gb25lIHBhc3NcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IG1vZGlmaWVycy5sZW5ndGg7IGkrKykge1xuICAgICAgY29uc3QgbW9kaWZpZXIgPSBtb2RpZmllcnNbaV07XG4gICAgICAvLyBDaGVjayBpZiBtb2RpZmllciBpcyBzZW5zaXRpdmUgKHN0YXJ0cyB3aXRoICdbJyBvciBpbiBvcmRlclNlbnNpdGl2ZU1vZGlmaWVycylcbiAgICAgIGNvbnN0IGlzQXJiaXRyYXJ5ID0gbW9kaWZpZXJbMF0gPT09ICdbJztcbiAgICAgIGNvbnN0IGlzT3JkZXJTZW5zaXRpdmUgPSBtb2RpZmllcldlaWdodHMuaGFzKG1vZGlmaWVyKTtcbiAgICAgIGlmIChpc0FyYml0cmFyeSB8fCBpc09yZGVyU2Vuc2l0aXZlKSB7XG4gICAgICAgIC8vIFNvcnQgYW5kIGZsdXNoIGN1cnJlbnQgc2VnbWVudCBhbHBoYWJldGljYWxseVxuICAgICAgICBpZiAoY3VycmVudFNlZ21lbnQubGVuZ3RoID4gMCkge1xuICAgICAgICAgIGN1cnJlbnRTZWdtZW50LnNvcnQoKTtcbiAgICAgICAgICByZXN1bHQucHVzaCguLi5jdXJyZW50U2VnbWVudCk7XG4gICAgICAgICAgY3VycmVudFNlZ21lbnQgPSBbXTtcbiAgICAgICAgfVxuICAgICAgICByZXN1bHQucHVzaChtb2RpZmllcik7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBSZWd1bGFyIG1vZGlmaWVyIC0gYWRkIHRvIGN1cnJlbnQgc2VnbWVudCBmb3IgYmF0Y2ggc29ydGluZ1xuICAgICAgICBjdXJyZW50U2VnbWVudC5wdXNoKG1vZGlmaWVyKTtcbiAgICAgIH1cbiAgICB9XG4gICAgLy8gU29ydCBhbmQgYWRkIGFueSByZW1haW5pbmcgc2VnbWVudCBpdGVtc1xuICAgIGlmIChjdXJyZW50U2VnbWVudC5sZW5ndGggPiAwKSB7XG4gICAgICBjdXJyZW50U2VnbWVudC5zb3J0KCk7XG4gICAgICByZXN1bHQucHVzaCguLi5jdXJyZW50U2VnbWVudCk7XG4gICAgfVxuICAgIHJldHVybiByZXN1bHQ7XG4gIH07XG59O1xuY29uc3QgY3JlYXRlQ29uZmlnVXRpbHMgPSBjb25maWcgPT4gKHtcbiAgY2FjaGU6IGNyZWF0ZUxydUNhY2hlKGNvbmZpZy5jYWNoZVNpemUpLFxuICBwYXJzZUNsYXNzTmFtZTogY3JlYXRlUGFyc2VDbGFzc05hbWUoY29uZmlnKSxcbiAgc29ydE1vZGlmaWVyczogY3JlYXRlU29ydE1vZGlmaWVycyhjb25maWcpLFxuICBwb3N0Zml4TG9va3VwQ2xhc3NHcm91cElkczogY3JlYXRlUG9zdGZpeExvb2t1cENsYXNzR3JvdXBJZHMoY29uZmlnKSxcbiAgLi4uY3JlYXRlQ2xhc3NHcm91cFV0aWxzKGNvbmZpZylcbn0pO1xuY29uc3QgY3JlYXRlUG9zdGZpeExvb2t1cENsYXNzR3JvdXBJZHMgPSBjb25maWcgPT4ge1xuICBjb25zdCBsb29rdXAgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuICBjb25zdCBjbGFzc0dyb3VwSWRzID0gY29uZmlnLnBvc3RmaXhMb29rdXBDbGFzc0dyb3VwcztcbiAgaWYgKGNsYXNzR3JvdXBJZHMpIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGNsYXNzR3JvdXBJZHMubGVuZ3RoOyBpKyspIHtcbiAgICAgIGxvb2t1cFtjbGFzc0dyb3VwSWRzW2ldXSA9IHRydWU7XG4gICAgfVxuICB9XG4gIHJldHVybiBsb29rdXA7XG59O1xuY29uc3QgU1BMSVRfQ0xBU1NFU19SRUdFWCA9IC9cXHMrLztcbmNvbnN0IG1lcmdlQ2xhc3NMaXN0ID0gKGNsYXNzTGlzdCwgY29uZmlnVXRpbHMpID0+IHtcbiAgY29uc3Qge1xuICAgIHBhcnNlQ2xhc3NOYW1lLFxuICAgIGdldENsYXNzR3JvdXBJZCxcbiAgICBnZXRDb25mbGljdGluZ0NsYXNzR3JvdXBJZHMsXG4gICAgc29ydE1vZGlmaWVycyxcbiAgICBwb3N0Zml4TG9va3VwQ2xhc3NHcm91cElkc1xuICB9ID0gY29uZmlnVXRpbHM7XG4gIC8qKlxuICAgKiBTZXQgb2YgY2xhc3NHcm91cElkcyBpbiBmb2xsb3dpbmcgZm9ybWF0OlxuICAgKiBge2ltcG9ydGFudE1vZGlmaWVyfXt2YXJpYW50TW9kaWZpZXJzfXtjbGFzc0dyb3VwSWR9YFxuICAgKiBAZXhhbXBsZSAnZmxvYXQnXG4gICAqIEBleGFtcGxlICdob3Zlcjpmb2N1czpiZy1jb2xvcidcbiAgICogQGV4YW1wbGUgJ21kOiFwcidcbiAgICovXG4gIGNvbnN0IGNsYXNzR3JvdXBzSW5Db25mbGljdCA9IFtdO1xuICBjb25zdCBjbGFzc05hbWVzID0gY2xhc3NMaXN0LnRyaW0oKS5zcGxpdChTUExJVF9DTEFTU0VTX1JFR0VYKTtcbiAgbGV0IHJlc3VsdCA9ICcnO1xuICBmb3IgKGxldCBpbmRleCA9IGNsYXNzTmFtZXMubGVuZ3RoIC0gMTsgaW5kZXggPj0gMDsgaW5kZXggLT0gMSkge1xuICAgIGNvbnN0IG9yaWdpbmFsQ2xhc3NOYW1lID0gY2xhc3NOYW1lc1tpbmRleF07XG4gICAgY29uc3Qge1xuICAgICAgaXNFeHRlcm5hbCxcbiAgICAgIG1vZGlmaWVycyxcbiAgICAgIGhhc0ltcG9ydGFudE1vZGlmaWVyLFxuICAgICAgYmFzZUNsYXNzTmFtZSxcbiAgICAgIG1heWJlUG9zdGZpeE1vZGlmaWVyUG9zaXRpb25cbiAgICB9ID0gcGFyc2VDbGFzc05hbWUob3JpZ2luYWxDbGFzc05hbWUpO1xuICAgIGlmIChpc0V4dGVybmFsKSB7XG4gICAgICByZXN1bHQgPSBvcmlnaW5hbENsYXNzTmFtZSArIChyZXN1bHQubGVuZ3RoID4gMCA/ICcgJyArIHJlc3VsdCA6IHJlc3VsdCk7XG4gICAgICBjb250aW51ZTtcbiAgICB9XG4gICAgbGV0IGhhc1Bvc3RmaXhNb2RpZmllciA9ICEhbWF5YmVQb3N0Zml4TW9kaWZpZXJQb3NpdGlvbjtcbiAgICBsZXQgY2xhc3NHcm91cElkO1xuICAgIGlmIChoYXNQb3N0Zml4TW9kaWZpZXIpIHtcbiAgICAgIGNvbnN0IGJhc2VDbGFzc05hbWVXaXRob3V0UG9zdGZpeCA9IGJhc2VDbGFzc05hbWUuc3Vic3RyaW5nKDAsIG1heWJlUG9zdGZpeE1vZGlmaWVyUG9zaXRpb24pO1xuICAgICAgY2xhc3NHcm91cElkID0gZ2V0Q2xhc3NHcm91cElkKGJhc2VDbGFzc05hbWVXaXRob3V0UG9zdGZpeCk7XG4gICAgICBjb25zdCBjbGFzc0dyb3VwSWRXaXRoUG9zdGZpeCA9IGNsYXNzR3JvdXBJZCAmJiBwb3N0Zml4TG9va3VwQ2xhc3NHcm91cElkc1tjbGFzc0dyb3VwSWRdID8gZ2V0Q2xhc3NHcm91cElkKGJhc2VDbGFzc05hbWUpIDogdW5kZWZpbmVkO1xuICAgICAgaWYgKGNsYXNzR3JvdXBJZFdpdGhQb3N0Zml4ICYmIGNsYXNzR3JvdXBJZFdpdGhQb3N0Zml4ICE9PSBjbGFzc0dyb3VwSWQpIHtcbiAgICAgICAgY2xhc3NHcm91cElkID0gY2xhc3NHcm91cElkV2l0aFBvc3RmaXg7XG4gICAgICAgIGhhc1Bvc3RmaXhNb2RpZmllciA9IGZhbHNlO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBjbGFzc0dyb3VwSWQgPSBnZXRDbGFzc0dyb3VwSWQoYmFzZUNsYXNzTmFtZSk7XG4gICAgfVxuICAgIGlmICghY2xhc3NHcm91cElkKSB7XG4gICAgICBpZiAoIWhhc1Bvc3RmaXhNb2RpZmllcikge1xuICAgICAgICAvLyBOb3QgYSBUYWlsd2luZCBjbGFzc1xuICAgICAgICByZXN1bHQgPSBvcmlnaW5hbENsYXNzTmFtZSArIChyZXN1bHQubGVuZ3RoID4gMCA/ICcgJyArIHJlc3VsdCA6IHJlc3VsdCk7XG4gICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuICAgICAgY2xhc3NHcm91cElkID0gZ2V0Q2xhc3NHcm91cElkKGJhc2VDbGFzc05hbWUpO1xuICAgICAgaWYgKCFjbGFzc0dyb3VwSWQpIHtcbiAgICAgICAgLy8gTm90IGEgVGFpbHdpbmQgY2xhc3NcbiAgICAgICAgcmVzdWx0ID0gb3JpZ2luYWxDbGFzc05hbWUgKyAocmVzdWx0Lmxlbmd0aCA+IDAgPyAnICcgKyByZXN1bHQgOiByZXN1bHQpO1xuICAgICAgICBjb250aW51ZTtcbiAgICAgIH1cbiAgICAgIGhhc1Bvc3RmaXhNb2RpZmllciA9IGZhbHNlO1xuICAgIH1cbiAgICAvLyBGYXN0IHBhdGg6IHNraXAgc29ydGluZyBmb3IgZW1wdHkgb3Igc2luZ2xlIG1vZGlmaWVyXG4gICAgY29uc3QgdmFyaWFudE1vZGlmaWVyID0gbW9kaWZpZXJzLmxlbmd0aCA9PT0gMCA/ICcnIDogbW9kaWZpZXJzLmxlbmd0aCA9PT0gMSA/IG1vZGlmaWVyc1swXSA6IHNvcnRNb2RpZmllcnMobW9kaWZpZXJzKS5qb2luKCc6Jyk7XG4gICAgY29uc3QgbW9kaWZpZXJJZCA9IGhhc0ltcG9ydGFudE1vZGlmaWVyID8gdmFyaWFudE1vZGlmaWVyICsgSU1QT1JUQU5UX01PRElGSUVSIDogdmFyaWFudE1vZGlmaWVyO1xuICAgIGNvbnN0IGNsYXNzSWQgPSBtb2RpZmllcklkICsgY2xhc3NHcm91cElkO1xuICAgIGlmIChjbGFzc0dyb3Vwc0luQ29uZmxpY3QuaW5kZXhPZihjbGFzc0lkKSA+IC0xKSB7XG4gICAgICAvLyBUYWlsd2luZCBjbGFzcyBvbWl0dGVkIGR1ZSB0byBjb25mbGljdFxuICAgICAgY29udGludWU7XG4gICAgfVxuICAgIGNsYXNzR3JvdXBzSW5Db25mbGljdC5wdXNoKGNsYXNzSWQpO1xuICAgIGNvbnN0IGNvbmZsaWN0R3JvdXBzID0gZ2V0Q29uZmxpY3RpbmdDbGFzc0dyb3VwSWRzKGNsYXNzR3JvdXBJZCwgaGFzUG9zdGZpeE1vZGlmaWVyKTtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGNvbmZsaWN0R3JvdXBzLmxlbmd0aDsgKytpKSB7XG4gICAgICBjb25zdCBncm91cCA9IGNvbmZsaWN0R3JvdXBzW2ldO1xuICAgICAgY2xhc3NHcm91cHNJbkNvbmZsaWN0LnB1c2gobW9kaWZpZXJJZCArIGdyb3VwKTtcbiAgICB9XG4gICAgLy8gVGFpbHdpbmQgY2xhc3Mgbm90IGluIGNvbmZsaWN0XG4gICAgcmVzdWx0ID0gb3JpZ2luYWxDbGFzc05hbWUgKyAocmVzdWx0Lmxlbmd0aCA+IDAgPyAnICcgKyByZXN1bHQgOiByZXN1bHQpO1xuICB9XG4gIHJldHVybiByZXN1bHQ7XG59O1xuXG4vKipcbiAqIFRoZSBjb2RlIGluIHRoaXMgZmlsZSBpcyBjb3BpZWQgZnJvbSBodHRwczovL2dpdGh1Yi5jb20vbHVrZWVkL2Nsc3ggYW5kIG1vZGlmaWVkIHRvIHN1aXQgdGhlIG5lZWRzIG9mIHRhaWx3aW5kLW1lcmdlIGJldHRlci5cbiAqXG4gKiBTcGVjaWZpY2FsbHk6XG4gKiAtIFJ1bnRpbWUgY29kZSBmcm9tIGh0dHBzOi8vZ2l0aHViLmNvbS9sdWtlZWQvY2xzeC9ibG9iL3YxLjIuMS9zcmMvaW5kZXguanNcbiAqIC0gVHlwZVNjcmlwdCB0eXBlcyBmcm9tIGh0dHBzOi8vZ2l0aHViLmNvbS9sdWtlZWQvY2xzeC9ibG9iL3YxLjIuMS9jbHN4LmQudHNcbiAqXG4gKiBPcmlnaW5hbCBjb2RlIGhhcyBNSVQgbGljZW5zZTogQ29weXJpZ2h0IChjKSBMdWtlIEVkd2FyZHMgPGx1a2UuZWR3YXJkczA1QGdtYWlsLmNvbT4gKGx1a2VlZC5jb20pXG4gKi9cbmNvbnN0IHR3Sm9pbiA9ICguLi5jbGFzc0xpc3RzKSA9PiB7XG4gIGxldCBpbmRleCA9IDA7XG4gIGxldCBhcmd1bWVudDtcbiAgbGV0IHJlc29sdmVkVmFsdWU7XG4gIGxldCBzdHJpbmcgPSAnJztcbiAgd2hpbGUgKGluZGV4IDwgY2xhc3NMaXN0cy5sZW5ndGgpIHtcbiAgICBpZiAoYXJndW1lbnQgPSBjbGFzc0xpc3RzW2luZGV4KytdKSB7XG4gICAgICBpZiAocmVzb2x2ZWRWYWx1ZSA9IHRvVmFsdWUoYXJndW1lbnQpKSB7XG4gICAgICAgIHN0cmluZyAmJiAoc3RyaW5nICs9ICcgJyk7XG4gICAgICAgIHN0cmluZyArPSByZXNvbHZlZFZhbHVlO1xuICAgICAgfVxuICAgIH1cbiAgfVxuICByZXR1cm4gc3RyaW5nO1xufTtcbmNvbnN0IHRvVmFsdWUgPSBtaXggPT4ge1xuICAvLyBGYXN0IHBhdGggZm9yIHN0cmluZ3NcbiAgaWYgKHR5cGVvZiBtaXggPT09ICdzdHJpbmcnKSB7XG4gICAgcmV0dXJuIG1peDtcbiAgfVxuICBsZXQgcmVzb2x2ZWRWYWx1ZTtcbiAgbGV0IHN0cmluZyA9ICcnO1xuICBmb3IgKGxldCBrID0gMDsgayA8IG1peC5sZW5ndGg7IGsrKykge1xuICAgIGlmIChtaXhba10pIHtcbiAgICAgIGlmIChyZXNvbHZlZFZhbHVlID0gdG9WYWx1ZShtaXhba10pKSB7XG4gICAgICAgIHN0cmluZyAmJiAoc3RyaW5nICs9ICcgJyk7XG4gICAgICAgIHN0cmluZyArPSByZXNvbHZlZFZhbHVlO1xuICAgICAgfVxuICAgIH1cbiAgfVxuICByZXR1cm4gc3RyaW5nO1xufTtcbmNvbnN0IGNyZWF0ZVRhaWx3aW5kTWVyZ2UgPSAoY3JlYXRlQ29uZmlnRmlyc3QsIC4uLmNyZWF0ZUNvbmZpZ1Jlc3QpID0+IHtcbiAgbGV0IGNvbmZpZ1V0aWxzO1xuICBsZXQgY2FjaGVHZXQ7XG4gIGxldCBjYWNoZVNldDtcbiAgbGV0IGZ1bmN0aW9uVG9DYWxsO1xuICBjb25zdCBpbml0VGFpbHdpbmRNZXJnZSA9IGNsYXNzTGlzdCA9PiB7XG4gICAgY29uc3QgY29uZmlnID0gY3JlYXRlQ29uZmlnUmVzdC5yZWR1Y2UoKHByZXZpb3VzQ29uZmlnLCBjcmVhdGVDb25maWdDdXJyZW50KSA9PiBjcmVhdGVDb25maWdDdXJyZW50KHByZXZpb3VzQ29uZmlnKSwgY3JlYXRlQ29uZmlnRmlyc3QoKSk7XG4gICAgY29uZmlnVXRpbHMgPSBjcmVhdGVDb25maWdVdGlscyhjb25maWcpO1xuICAgIGNhY2hlR2V0ID0gY29uZmlnVXRpbHMuY2FjaGUuZ2V0O1xuICAgIGNhY2hlU2V0ID0gY29uZmlnVXRpbHMuY2FjaGUuc2V0O1xuICAgIGZ1bmN0aW9uVG9DYWxsID0gdGFpbHdpbmRNZXJnZTtcbiAgICByZXR1cm4gdGFpbHdpbmRNZXJnZShjbGFzc0xpc3QpO1xuICB9O1xuICBjb25zdCB0YWlsd2luZE1lcmdlID0gY2xhc3NMaXN0ID0+IHtcbiAgICBjb25zdCBjYWNoZWRSZXN1bHQgPSBjYWNoZUdldChjbGFzc0xpc3QpO1xuICAgIGlmIChjYWNoZWRSZXN1bHQpIHtcbiAgICAgIHJldHVybiBjYWNoZWRSZXN1bHQ7XG4gICAgfVxuICAgIGNvbnN0IHJlc3VsdCA9IG1lcmdlQ2xhc3NMaXN0KGNsYXNzTGlzdCwgY29uZmlnVXRpbHMpO1xuICAgIGNhY2hlU2V0KGNsYXNzTGlzdCwgcmVzdWx0KTtcbiAgICByZXR1cm4gcmVzdWx0O1xuICB9O1xuICBmdW5jdGlvblRvQ2FsbCA9IGluaXRUYWlsd2luZE1lcmdlO1xuICByZXR1cm4gKC4uLmFyZ3MpID0+IGZ1bmN0aW9uVG9DYWxsKHR3Sm9pbiguLi5hcmdzKSk7XG59O1xuY29uc3QgZmFsbGJhY2tUaGVtZUFyciA9IFtdO1xuY29uc3QgZnJvbVRoZW1lID0ga2V5ID0+IHtcbiAgY29uc3QgdGhlbWVHZXR0ZXIgPSB0aGVtZSA9PiB0aGVtZVtrZXldIHx8IGZhbGxiYWNrVGhlbWVBcnI7XG4gIHRoZW1lR2V0dGVyLmlzVGhlbWVHZXR0ZXIgPSB0cnVlO1xuICByZXR1cm4gdGhlbWVHZXR0ZXI7XG59O1xuY29uc3QgYXJiaXRyYXJ5VmFsdWVSZWdleCA9IC9eXFxbKD86KFxcd1tcXHctXSopOik/KC4rKVxcXSQvaTtcbmNvbnN0IGFyYml0cmFyeVZhcmlhYmxlUmVnZXggPSAvXlxcKCg/OihcXHdbXFx3LV0qKTopPyguKylcXCkkL2k7XG5jb25zdCBmcmFjdGlvblJlZ2V4ID0gL15cXGQrKD86XFwuXFxkKyk/XFwvXFxkKyg/OlxcLlxcZCspPyQvO1xuY29uc3QgdHNoaXJ0VW5pdFJlZ2V4ID0gL14oXFxkKyhcXC5cXGQrKT8pPyh4c3xzbXxtZHxsZ3x4bCkkLztcbmNvbnN0IGxlbmd0aFVuaXRSZWdleCA9IC9cXGQrKCV8cHh8cj9lbXxbc2RsXT92KFtod2liXXxtaW58bWF4KXxwdHxwY3xpbnxjbXxtbXxjYXB8Y2h8ZXh8cj9saHxjcSh3fGh8aXxifG1pbnxtYXgpKXxcXGIoY2FsY3xtaW58bWF4fGNsYW1wKVxcKC4rXFwpfF4wJC87XG5jb25zdCBjb2xvckZ1bmN0aW9uUmVnZXggPSAvXihyZ2JhP3xoc2xhP3xod2J8KG9rKT8obGFifGxjaCl8Y29sb3ItbWl4KVxcKC4rXFwpJC87XG4vLyBTaGFkb3cgYWx3YXlzIGJlZ2lucyB3aXRoIHggYW5kIHkgb2Zmc2V0IHNlcGFyYXRlZCBieSB1bmRlcnNjb3JlIG9wdGlvbmFsbHkgcHJlcGVuZGVkIGJ5IGluc2V0XG5jb25zdCBzaGFkb3dSZWdleCA9IC9eKGluc2V0Xyk/LT8oKFxcZCspP1xcLj8oXFxkKylbYS16XSt8MClfLT8oKFxcZCspP1xcLj8oXFxkKylbYS16XSt8MCkvO1xuY29uc3QgaW1hZ2VSZWdleCA9IC9eKHVybHxpbWFnZXxpbWFnZS1zZXR8Y3Jvc3MtZmFkZXxlbGVtZW50fChyZXBlYXRpbmctKT8obGluZWFyfHJhZGlhbHxjb25pYyktZ3JhZGllbnQpXFwoLitcXCkkLztcbmNvbnN0IGlzRnJhY3Rpb24gPSB2YWx1ZSA9PiBmcmFjdGlvblJlZ2V4LnRlc3QodmFsdWUpO1xuY29uc3QgaXNOdW1iZXIgPSB2YWx1ZSA9PiAhIXZhbHVlICYmICFOdW1iZXIuaXNOYU4oTnVtYmVyKHZhbHVlKSk7XG5jb25zdCBpc0ludGVnZXIgPSB2YWx1ZSA9PiAhIXZhbHVlICYmIE51bWJlci5pc0ludGVnZXIoTnVtYmVyKHZhbHVlKSk7XG5jb25zdCBpc1BlcmNlbnQgPSB2YWx1ZSA9PiB2YWx1ZS5lbmRzV2l0aCgnJScpICYmIGlzTnVtYmVyKHZhbHVlLnNsaWNlKDAsIC0xKSk7XG5jb25zdCBpc1RzaGlydFNpemUgPSB2YWx1ZSA9PiB0c2hpcnRVbml0UmVnZXgudGVzdCh2YWx1ZSk7XG5jb25zdCBpc0FueSA9ICgpID0+IHRydWU7XG5jb25zdCBpc0xlbmd0aE9ubHkgPSB2YWx1ZSA9PlxuLy8gYGNvbG9yRnVuY3Rpb25SZWdleGAgY2hlY2sgaXMgbmVjZXNzYXJ5IGJlY2F1c2UgY29sb3IgZnVuY3Rpb25zIGNhbiBoYXZlIHBlcmNlbnRhZ2VzIGluIHRoZW0gd2hpY2ggd2hpY2ggd291bGQgYmUgaW5jb3JyZWN0bHkgY2xhc3NpZmllZCBhcyBsZW5ndGhzLlxuLy8gRm9yIGV4YW1wbGUsIGBoc2woMCAwJSAwJSlgIHdvdWxkIGJlIGNsYXNzaWZpZWQgYXMgYSBsZW5ndGggd2l0aG91dCB0aGlzIGNoZWNrLlxuLy8gSSBjb3VsZCBhbHNvIHVzZSBsb29rYmVoaW5kIGFzc2VydGlvbiBpbiBgbGVuZ3RoVW5pdFJlZ2V4YCBidXQgdGhhdCBpc24ndCBzdXBwb3J0ZWQgd2lkZWx5IGVub3VnaC5cbmxlbmd0aFVuaXRSZWdleC50ZXN0KHZhbHVlKSAmJiAhY29sb3JGdW5jdGlvblJlZ2V4LnRlc3QodmFsdWUpO1xuY29uc3QgaXNOZXZlciA9ICgpID0+IGZhbHNlO1xuY29uc3QgaXNTaGFkb3cgPSB2YWx1ZSA9PiBzaGFkb3dSZWdleC50ZXN0KHZhbHVlKTtcbmNvbnN0IGlzSW1hZ2UgPSB2YWx1ZSA9PiBpbWFnZVJlZ2V4LnRlc3QodmFsdWUpO1xuY29uc3QgaXNBbnlOb25BcmJpdHJhcnkgPSB2YWx1ZSA9PiAhaXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSkgJiYgIWlzQXJiaXRyYXJ5VmFyaWFibGUodmFsdWUpO1xuY29uc3QgaXNOYW1lZENvbnRhaW5lclF1ZXJ5ID0gdmFsdWUgPT4gdmFsdWUuc3RhcnRzV2l0aCgnQGNvbnRhaW5lcicpICYmICh2YWx1ZVsxMF0gPT09ICcvJyAmJiB2YWx1ZVsxMV0gIT09IHVuZGVmaW5lZCB8fCB2YWx1ZVsxMV0gPT09ICdzJyAmJiB2YWx1ZVsxNl0gIT09IHVuZGVmaW5lZCAmJiB2YWx1ZS5zdGFydHNXaXRoKCctc2l6ZS8nLCAxMCkgfHwgdmFsdWVbMTFdID09PSAnbicgJiYgdmFsdWVbMThdICE9PSB1bmRlZmluZWQgJiYgdmFsdWUuc3RhcnRzV2l0aCgnLW5vcm1hbC8nLCAxMCkpO1xuY29uc3QgaXNBcmJpdHJhcnlTaXplID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSwgaXNMYWJlbFNpemUsIGlzTmV2ZXIpO1xuY29uc3QgaXNBcmJpdHJhcnlWYWx1ZSA9IHZhbHVlID0+IGFyYml0cmFyeVZhbHVlUmVnZXgudGVzdCh2YWx1ZSk7XG5jb25zdCBpc0FyYml0cmFyeUxlbmd0aCA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFsdWUodmFsdWUsIGlzTGFiZWxMZW5ndGgsIGlzTGVuZ3RoT25seSk7XG5jb25zdCBpc0FyYml0cmFyeU51bWJlciA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFsdWUodmFsdWUsIGlzTGFiZWxOdW1iZXIsIGlzTnVtYmVyKTtcbmNvbnN0IGlzQXJiaXRyYXJ5V2VpZ2h0ID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSwgaXNMYWJlbFdlaWdodCwgaXNBbnkpO1xuY29uc3QgaXNBcmJpdHJhcnlGYW1pbHlOYW1lID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSwgaXNMYWJlbEZhbWlseU5hbWUsIGlzTmV2ZXIpO1xuY29uc3QgaXNBcmJpdHJhcnlQb3NpdGlvbiA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFsdWUodmFsdWUsIGlzTGFiZWxQb3NpdGlvbiwgaXNOZXZlcik7XG5jb25zdCBpc0FyYml0cmFyeUltYWdlID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSwgaXNMYWJlbEltYWdlLCBpc0ltYWdlKTtcbmNvbnN0IGlzQXJiaXRyYXJ5U2hhZG93ID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYWx1ZSh2YWx1ZSwgaXNMYWJlbFNoYWRvdywgaXNTaGFkb3cpO1xuY29uc3QgaXNBcmJpdHJhcnlWYXJpYWJsZSA9IHZhbHVlID0+IGFyYml0cmFyeVZhcmlhYmxlUmVnZXgudGVzdCh2YWx1ZSk7XG5jb25zdCBpc0FyYml0cmFyeVZhcmlhYmxlTGVuZ3RoID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYXJpYWJsZSh2YWx1ZSwgaXNMYWJlbExlbmd0aCk7XG5jb25zdCBpc0FyYml0cmFyeVZhcmlhYmxlRmFtaWx5TmFtZSA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFyaWFibGUodmFsdWUsIGlzTGFiZWxGYW1pbHlOYW1lKTtcbmNvbnN0IGlzQXJiaXRyYXJ5VmFyaWFibGVQb3NpdGlvbiA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFyaWFibGUodmFsdWUsIGlzTGFiZWxQb3NpdGlvbik7XG5jb25zdCBpc0FyYml0cmFyeVZhcmlhYmxlU2l6ZSA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFyaWFibGUodmFsdWUsIGlzTGFiZWxTaXplKTtcbmNvbnN0IGlzQXJiaXRyYXJ5VmFyaWFibGVJbWFnZSA9IHZhbHVlID0+IGdldElzQXJiaXRyYXJ5VmFyaWFibGUodmFsdWUsIGlzTGFiZWxJbWFnZSk7XG5jb25zdCBpc0FyYml0cmFyeVZhcmlhYmxlU2hhZG93ID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYXJpYWJsZSh2YWx1ZSwgaXNMYWJlbFNoYWRvdywgdHJ1ZSk7XG5jb25zdCBpc0FyYml0cmFyeVZhcmlhYmxlV2VpZ2h0ID0gdmFsdWUgPT4gZ2V0SXNBcmJpdHJhcnlWYXJpYWJsZSh2YWx1ZSwgaXNMYWJlbFdlaWdodCwgdHJ1ZSk7XG4vLyBIZWxwZXJzXG5jb25zdCBnZXRJc0FyYml0cmFyeVZhbHVlID0gKHZhbHVlLCB0ZXN0TGFiZWwsIHRlc3RWYWx1ZSkgPT4ge1xuICBjb25zdCByZXN1bHQgPSBhcmJpdHJhcnlWYWx1ZVJlZ2V4LmV4ZWModmFsdWUpO1xuICBpZiAocmVzdWx0KSB7XG4gICAgaWYgKHJlc3VsdFsxXSkge1xuICAgICAgcmV0dXJuIHRlc3RMYWJlbChyZXN1bHRbMV0pO1xuICAgIH1cbiAgICByZXR1cm4gdGVzdFZhbHVlKHJlc3VsdFsyXSk7XG4gIH1cbiAgcmV0dXJuIGZhbHNlO1xufTtcbmNvbnN0IGdldElzQXJiaXRyYXJ5VmFyaWFibGUgPSAodmFsdWUsIHRlc3RMYWJlbCwgc2hvdWxkTWF0Y2hOb0xhYmVsID0gZmFsc2UpID0+IHtcbiAgY29uc3QgcmVzdWx0ID0gYXJiaXRyYXJ5VmFyaWFibGVSZWdleC5leGVjKHZhbHVlKTtcbiAgaWYgKHJlc3VsdCkge1xuICAgIGlmIChyZXN1bHRbMV0pIHtcbiAgICAgIHJldHVybiB0ZXN0TGFiZWwocmVzdWx0WzFdKTtcbiAgICB9XG4gICAgcmV0dXJuIHNob3VsZE1hdGNoTm9MYWJlbDtcbiAgfVxuICByZXR1cm4gZmFsc2U7XG59O1xuLy8gTGFiZWxzXG5jb25zdCBpc0xhYmVsUG9zaXRpb24gPSBsYWJlbCA9PiBsYWJlbCA9PT0gJ3Bvc2l0aW9uJyB8fCBsYWJlbCA9PT0gJ3BlcmNlbnRhZ2UnO1xuY29uc3QgaXNMYWJlbEltYWdlID0gbGFiZWwgPT4gbGFiZWwgPT09ICdpbWFnZScgfHwgbGFiZWwgPT09ICd1cmwnO1xuY29uc3QgaXNMYWJlbFNpemUgPSBsYWJlbCA9PiBsYWJlbCA9PT0gJ2xlbmd0aCcgfHwgbGFiZWwgPT09ICdzaXplJyB8fCBsYWJlbCA9PT0gJ2JnLXNpemUnO1xuY29uc3QgaXNMYWJlbExlbmd0aCA9IGxhYmVsID0+IGxhYmVsID09PSAnbGVuZ3RoJztcbmNvbnN0IGlzTGFiZWxOdW1iZXIgPSBsYWJlbCA9PiBsYWJlbCA9PT0gJ251bWJlcic7XG5jb25zdCBpc0xhYmVsRmFtaWx5TmFtZSA9IGxhYmVsID0+IGxhYmVsID09PSAnZmFtaWx5LW5hbWUnO1xuY29uc3QgaXNMYWJlbFdlaWdodCA9IGxhYmVsID0+IGxhYmVsID09PSAnbnVtYmVyJyB8fCBsYWJlbCA9PT0gJ3dlaWdodCc7XG5jb25zdCBpc0xhYmVsU2hhZG93ID0gbGFiZWwgPT4gbGFiZWwgPT09ICdzaGFkb3cnO1xuY29uc3QgdmFsaWRhdG9ycyA9IC8qI19fUFVSRV9fKi9PYmplY3QuZGVmaW5lUHJvcGVydHkoe1xuICBfX3Byb3RvX186IG51bGwsXG4gIGlzQW55LFxuICBpc0FueU5vbkFyYml0cmFyeSxcbiAgaXNBcmJpdHJhcnlGYW1pbHlOYW1lLFxuICBpc0FyYml0cmFyeUltYWdlLFxuICBpc0FyYml0cmFyeUxlbmd0aCxcbiAgaXNBcmJpdHJhcnlOdW1iZXIsXG4gIGlzQXJiaXRyYXJ5UG9zaXRpb24sXG4gIGlzQXJiaXRyYXJ5U2hhZG93LFxuICBpc0FyYml0cmFyeVNpemUsXG4gIGlzQXJiaXRyYXJ5VmFsdWUsXG4gIGlzQXJiaXRyYXJ5VmFyaWFibGUsXG4gIGlzQXJiaXRyYXJ5VmFyaWFibGVGYW1pbHlOYW1lLFxuICBpc0FyYml0cmFyeVZhcmlhYmxlSW1hZ2UsXG4gIGlzQXJiaXRyYXJ5VmFyaWFibGVMZW5ndGgsXG4gIGlzQXJiaXRyYXJ5VmFyaWFibGVQb3NpdGlvbixcbiAgaXNBcmJpdHJhcnlWYXJpYWJsZVNoYWRvdyxcbiAgaXNBcmJpdHJhcnlWYXJpYWJsZVNpemUsXG4gIGlzQXJiaXRyYXJ5VmFyaWFibGVXZWlnaHQsXG4gIGlzQXJiaXRyYXJ5V2VpZ2h0LFxuICBpc0ZyYWN0aW9uLFxuICBpc0ludGVnZXIsXG4gIGlzTmFtZWRDb250YWluZXJRdWVyeSxcbiAgaXNOdW1iZXIsXG4gIGlzUGVyY2VudCxcbiAgaXNUc2hpcnRTaXplXG59LCBTeW1ib2wudG9TdHJpbmdUYWcsIHtcbiAgdmFsdWU6ICdNb2R1bGUnXG59KTtcbmNvbnN0IGdldERlZmF1bHRDb25maWcgPSAoKSA9PiB7XG4gIC8qKlxuICAgKiBUaGVtZSBnZXR0ZXJzIGZvciB0aGVtZSB2YXJpYWJsZSBuYW1lc3BhY2VzXG4gICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90aGVtZSN0aGVtZS12YXJpYWJsZS1uYW1lc3BhY2VzXG4gICAqL1xuICAvKioqL1xuICBjb25zdCB0aGVtZUNvbG9yID0gZnJvbVRoZW1lKCdjb2xvcicpO1xuICBjb25zdCB0aGVtZUZvbnQgPSBmcm9tVGhlbWUoJ2ZvbnQnKTtcbiAgY29uc3QgdGhlbWVUZXh0ID0gZnJvbVRoZW1lKCd0ZXh0Jyk7XG4gIGNvbnN0IHRoZW1lRm9udFdlaWdodCA9IGZyb21UaGVtZSgnZm9udC13ZWlnaHQnKTtcbiAgY29uc3QgdGhlbWVUcmFja2luZyA9IGZyb21UaGVtZSgndHJhY2tpbmcnKTtcbiAgY29uc3QgdGhlbWVMZWFkaW5nID0gZnJvbVRoZW1lKCdsZWFkaW5nJyk7XG4gIGNvbnN0IHRoZW1lQnJlYWtwb2ludCA9IGZyb21UaGVtZSgnYnJlYWtwb2ludCcpO1xuICBjb25zdCB0aGVtZUNvbnRhaW5lciA9IGZyb21UaGVtZSgnY29udGFpbmVyJyk7XG4gIGNvbnN0IHRoZW1lU3BhY2luZyA9IGZyb21UaGVtZSgnc3BhY2luZycpO1xuICBjb25zdCB0aGVtZVJhZGl1cyA9IGZyb21UaGVtZSgncmFkaXVzJyk7XG4gIGNvbnN0IHRoZW1lU2hhZG93ID0gZnJvbVRoZW1lKCdzaGFkb3cnKTtcbiAgY29uc3QgdGhlbWVJbnNldFNoYWRvdyA9IGZyb21UaGVtZSgnaW5zZXQtc2hhZG93Jyk7XG4gIGNvbnN0IHRoZW1lVGV4dFNoYWRvdyA9IGZyb21UaGVtZSgndGV4dC1zaGFkb3cnKTtcbiAgY29uc3QgdGhlbWVEcm9wU2hhZG93ID0gZnJvbVRoZW1lKCdkcm9wLXNoYWRvdycpO1xuICBjb25zdCB0aGVtZUJsdXIgPSBmcm9tVGhlbWUoJ2JsdXInKTtcbiAgY29uc3QgdGhlbWVQZXJzcGVjdGl2ZSA9IGZyb21UaGVtZSgncGVyc3BlY3RpdmUnKTtcbiAgY29uc3QgdGhlbWVBc3BlY3QgPSBmcm9tVGhlbWUoJ2FzcGVjdCcpO1xuICBjb25zdCB0aGVtZUVhc2UgPSBmcm9tVGhlbWUoJ2Vhc2UnKTtcbiAgY29uc3QgdGhlbWVBbmltYXRlID0gZnJvbVRoZW1lKCdhbmltYXRlJyk7XG4gIC8qKlxuICAgKiBIZWxwZXJzIHRvIGF2b2lkIHJlcGVhdGluZyB0aGUgc2FtZSBzY2FsZXNcbiAgICpcbiAgICogV2UgdXNlIGZ1bmN0aW9ucyB0aGF0IGNyZWF0ZSBhIG5ldyBhcnJheSBldmVyeSB0aW1lIHRoZXkncmUgY2FsbGVkIGluc3RlYWQgb2Ygc3RhdGljIGFycmF5cy5cbiAgICogVGhpcyBlbnN1cmVzIHRoYXQgdXNlcnMgd2hvIG1vZGlmeSBhbnkgc2NhbGUgYnkgbXV0YXRpbmcgdGhlIGFycmF5IChlLmcuIHdpdGggYGFycmF5LnB1c2goZWxlbWVudClgKSBkb24ndCBhY2NpZGVudGFsbHkgbXV0YXRlIGFycmF5cyBpbiBvdGhlciBwYXJ0cyBvZiB0aGUgY29uZmlnLlxuICAgKi9cbiAgLyoqKi9cbiAgY29uc3Qgc2NhbGVCcmVhayA9ICgpID0+IFsnYXV0bycsICdhdm9pZCcsICdhbGwnLCAnYXZvaWQtcGFnZScsICdwYWdlJywgJ2xlZnQnLCAncmlnaHQnLCAnY29sdW1uJ107XG4gIGNvbnN0IHNjYWxlUG9zaXRpb24gPSAoKSA9PiBbJ2NlbnRlcicsICd0b3AnLCAnYm90dG9tJywgJ2xlZnQnLCAncmlnaHQnLCAndG9wLWxlZnQnLFxuICAvLyBEZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4xLjAsIHNlZSBodHRwczovL2dpdGh1Yi5jb20vdGFpbHdpbmRsYWJzL3RhaWx3aW5kY3NzL3B1bGwvMTczNzhcbiAgJ2xlZnQtdG9wJywgJ3RvcC1yaWdodCcsXG4gIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjEuMCwgc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS90YWlsd2luZGxhYnMvdGFpbHdpbmRjc3MvcHVsbC8xNzM3OFxuICAncmlnaHQtdG9wJywgJ2JvdHRvbS1yaWdodCcsXG4gIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjEuMCwgc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS90YWlsd2luZGxhYnMvdGFpbHdpbmRjc3MvcHVsbC8xNzM3OFxuICAncmlnaHQtYm90dG9tJywgJ2JvdHRvbS1sZWZ0JyxcbiAgLy8gRGVwcmVjYXRlZCBzaW5jZSBUYWlsd2luZCBDU1MgdjQuMS4wLCBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy9wdWxsLzE3Mzc4XG4gICdsZWZ0LWJvdHRvbSddO1xuICBjb25zdCBzY2FsZVBvc2l0aW9uV2l0aEFyYml0cmFyeSA9ICgpID0+IFsuLi5zY2FsZVBvc2l0aW9uKCksIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdO1xuICBjb25zdCBzY2FsZU92ZXJmbG93ID0gKCkgPT4gWydhdXRvJywgJ2hpZGRlbicsICdjbGlwJywgJ3Zpc2libGUnLCAnc2Nyb2xsJ107XG4gIGNvbnN0IHNjYWxlT3ZlcnNjcm9sbCA9ICgpID0+IFsnYXV0bycsICdjb250YWluJywgJ25vbmUnXTtcbiAgY29uc3Qgc2NhbGVVbmFtYmlndW91c1NwYWNpbmcgPSAoKSA9PiBbaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZSwgdGhlbWVTcGFjaW5nXTtcbiAgY29uc3Qgc2NhbGVJbnNldCA9ICgpID0+IFtpc0ZyYWN0aW9uLCAnZnVsbCcsICdhdXRvJywgLi4uc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKV07XG4gIGNvbnN0IHNjYWxlR3JpZFRlbXBsYXRlQ29sc1Jvd3MgPSAoKSA9PiBbaXNJbnRlZ2VyLCAnbm9uZScsICdzdWJncmlkJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV07XG4gIGNvbnN0IHNjYWxlR3JpZENvbFJvd1N0YXJ0QW5kRW5kID0gKCkgPT4gWydhdXRvJywge1xuICAgIHNwYW46IFsnZnVsbCcsIGlzSW50ZWdlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgfSwgaXNJbnRlZ2VyLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXTtcbiAgY29uc3Qgc2NhbGVHcmlkQ29sUm93U3RhcnRPckVuZCA9ICgpID0+IFtpc0ludGVnZXIsICdhdXRvJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV07XG4gIGNvbnN0IHNjYWxlR3JpZEF1dG9Db2xzUm93cyA9ICgpID0+IFsnYXV0bycsICdtaW4nLCAnbWF4JywgJ2ZyJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV07XG4gIGNvbnN0IHNjYWxlQWxpZ25QcmltYXJ5QXhpcyA9ICgpID0+IFsnc3RhcnQnLCAnZW5kJywgJ2NlbnRlcicsICdiZXR3ZWVuJywgJ2Fyb3VuZCcsICdldmVubHknLCAnc3RyZXRjaCcsICdiYXNlbGluZScsICdjZW50ZXItc2FmZScsICdlbmQtc2FmZSddO1xuICBjb25zdCBzY2FsZUFsaWduU2Vjb25kYXJ5QXhpcyA9ICgpID0+IFsnc3RhcnQnLCAnZW5kJywgJ2NlbnRlcicsICdzdHJldGNoJywgJ2NlbnRlci1zYWZlJywgJ2VuZC1zYWZlJ107XG4gIGNvbnN0IHNjYWxlTWFyZ2luID0gKCkgPT4gWydhdXRvJywgLi4uc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKV07XG4gIGNvbnN0IHNjYWxlU2l6aW5nID0gKCkgPT4gW2lzRnJhY3Rpb24sICdhdXRvJywgJ2Z1bGwnLCAnZHZ3JywgJ2R2aCcsICdsdncnLCAnbHZoJywgJ3N2dycsICdzdmgnLCAnbWluJywgJ21heCcsICdmaXQnLCAuLi5zY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXTtcbiAgY29uc3Qgc2NhbGVTaXppbmdJbmxpbmUgPSAoKSA9PiBbaXNGcmFjdGlvbiwgJ3NjcmVlbicsICdmdWxsJywgJ2R2dycsICdsdncnLCAnc3Z3JywgJ21pbicsICdtYXgnLCAnZml0JywgLi4uc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKV07XG4gIGNvbnN0IHNjYWxlU2l6aW5nQmxvY2sgPSAoKSA9PiBbaXNGcmFjdGlvbiwgJ3NjcmVlbicsICdmdWxsJywgJ2xoJywgJ2R2aCcsICdsdmgnLCAnc3ZoJywgJ21pbicsICdtYXgnLCAnZml0JywgLi4uc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKV07XG4gIGNvbnN0IHNjYWxlQ29sb3IgPSAoKSA9PiBbdGhlbWVDb2xvciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV07XG4gIGNvbnN0IHNjYWxlQmdQb3NpdGlvbiA9ICgpID0+IFsuLi5zY2FsZVBvc2l0aW9uKCksIGlzQXJiaXRyYXJ5VmFyaWFibGVQb3NpdGlvbiwgaXNBcmJpdHJhcnlQb3NpdGlvbiwge1xuICAgIHBvc2l0aW9uOiBbaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgfV07XG4gIGNvbnN0IHNjYWxlQmdSZXBlYXQgPSAoKSA9PiBbJ25vLXJlcGVhdCcsIHtcbiAgICByZXBlYXQ6IFsnJywgJ3gnLCAneScsICdzcGFjZScsICdyb3VuZCddXG4gIH1dO1xuICBjb25zdCBzY2FsZUJnU2l6ZSA9ICgpID0+IFsnYXV0bycsICdjb3ZlcicsICdjb250YWluJywgaXNBcmJpdHJhcnlWYXJpYWJsZVNpemUsIGlzQXJiaXRyYXJ5U2l6ZSwge1xuICAgIHNpemU6IFtpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICB9XTtcbiAgY29uc3Qgc2NhbGVHcmFkaWVudFN0b3BQb3NpdGlvbiA9ICgpID0+IFtpc1BlcmNlbnQsIGlzQXJiaXRyYXJ5VmFyaWFibGVMZW5ndGgsIGlzQXJiaXRyYXJ5TGVuZ3RoXTtcbiAgY29uc3Qgc2NhbGVSYWRpdXMgPSAoKSA9PiBbXG4gIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjAuMFxuICAnJywgJ25vbmUnLCAnZnVsbCcsIHRoZW1lUmFkaXVzLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXTtcbiAgY29uc3Qgc2NhbGVCb3JkZXJXaWR0aCA9ICgpID0+IFsnJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGVMZW5ndGgsIGlzQXJiaXRyYXJ5TGVuZ3RoXTtcbiAgY29uc3Qgc2NhbGVMaW5lU3R5bGUgPSAoKSA9PiBbJ3NvbGlkJywgJ2Rhc2hlZCcsICdkb3R0ZWQnLCAnZG91YmxlJ107XG4gIGNvbnN0IHNjYWxlQmxlbmRNb2RlID0gKCkgPT4gWydub3JtYWwnLCAnbXVsdGlwbHknLCAnc2NyZWVuJywgJ292ZXJsYXknLCAnZGFya2VuJywgJ2xpZ2h0ZW4nLCAnY29sb3ItZG9kZ2UnLCAnY29sb3ItYnVybicsICdoYXJkLWxpZ2h0JywgJ3NvZnQtbGlnaHQnLCAnZGlmZmVyZW5jZScsICdleGNsdXNpb24nLCAnaHVlJywgJ3NhdHVyYXRpb24nLCAnY29sb3InLCAnbHVtaW5vc2l0eSddO1xuICBjb25zdCBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uID0gKCkgPT4gW2lzTnVtYmVyLCBpc1BlcmNlbnQsIGlzQXJiaXRyYXJ5VmFyaWFibGVQb3NpdGlvbiwgaXNBcmJpdHJhcnlQb3NpdGlvbl07XG4gIGNvbnN0IHNjYWxlQmx1ciA9ICgpID0+IFtcbiAgLy8gRGVwcmVjYXRlZCBzaW5jZSBUYWlsd2luZCBDU1MgdjQuMC4wXG4gICcnLCAnbm9uZScsIHRoZW1lQmx1ciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV07XG4gIGNvbnN0IHNjYWxlUm90YXRlID0gKCkgPT4gWydub25lJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdO1xuICBjb25zdCBzY2FsZVNjYWxlID0gKCkgPT4gWydub25lJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdO1xuICBjb25zdCBzY2FsZVNrZXcgPSAoKSA9PiBbaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdO1xuICBjb25zdCBzY2FsZVRyYW5zbGF0ZSA9ICgpID0+IFtpc0ZyYWN0aW9uLCAnZnVsbCcsIC4uLnNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKCldO1xuICByZXR1cm4ge1xuICAgIGNhY2hlU2l6ZTogNTAwLFxuICAgIHRoZW1lOiB7XG4gICAgICBhbmltYXRlOiBbJ3NwaW4nLCAncGluZycsICdwdWxzZScsICdib3VuY2UnXSxcbiAgICAgIGFzcGVjdDogWyd2aWRlbyddLFxuICAgICAgYmx1cjogW2lzVHNoaXJ0U2l6ZV0sXG4gICAgICBicmVha3BvaW50OiBbaXNUc2hpcnRTaXplXSxcbiAgICAgIGNvbG9yOiBbaXNBbnldLFxuICAgICAgY29udGFpbmVyOiBbaXNUc2hpcnRTaXplXSxcbiAgICAgICdkcm9wLXNoYWRvdyc6IFtpc1RzaGlydFNpemVdLFxuICAgICAgZWFzZTogWydpbicsICdvdXQnLCAnaW4tb3V0J10sXG4gICAgICBmb250OiBbaXNBbnlOb25BcmJpdHJhcnldLFxuICAgICAgJ2ZvbnQtd2VpZ2h0JzogWyd0aGluJywgJ2V4dHJhbGlnaHQnLCAnbGlnaHQnLCAnbm9ybWFsJywgJ21lZGl1bScsICdzZW1pYm9sZCcsICdib2xkJywgJ2V4dHJhYm9sZCcsICdibGFjayddLFxuICAgICAgJ2luc2V0LXNoYWRvdyc6IFtpc1RzaGlydFNpemVdLFxuICAgICAgbGVhZGluZzogWydub25lJywgJ3RpZ2h0JywgJ3NudWcnLCAnbm9ybWFsJywgJ3JlbGF4ZWQnLCAnbG9vc2UnXSxcbiAgICAgIHBlcnNwZWN0aXZlOiBbJ2RyYW1hdGljJywgJ25lYXInLCAnbm9ybWFsJywgJ21pZHJhbmdlJywgJ2Rpc3RhbnQnLCAnbm9uZSddLFxuICAgICAgcmFkaXVzOiBbaXNUc2hpcnRTaXplXSxcbiAgICAgIHNoYWRvdzogW2lzVHNoaXJ0U2l6ZV0sXG4gICAgICBzcGFjaW5nOiBbJ3B4JywgaXNOdW1iZXJdLFxuICAgICAgdGV4dDogW2lzVHNoaXJ0U2l6ZV0sXG4gICAgICAndGV4dC1zaGFkb3cnOiBbaXNUc2hpcnRTaXplXSxcbiAgICAgIHRyYWNraW5nOiBbJ3RpZ2h0ZXInLCAndGlnaHQnLCAnbm9ybWFsJywgJ3dpZGUnLCAnd2lkZXInLCAnd2lkZXN0J11cbiAgICB9LFxuICAgIGNsYXNzR3JvdXBzOiB7XG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLVxuICAgICAgLy8gLS0tIExheW91dCAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tXG4gICAgICAvKipcbiAgICAgICAqIEFzcGVjdCBSYXRpb1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2FzcGVjdC1yYXRpb1xuICAgICAgICovXG4gICAgICBhc3BlY3Q6IFt7XG4gICAgICAgIGFzcGVjdDogWydhdXRvJywgJ3NxdWFyZScsIGlzRnJhY3Rpb24sIGlzQXJiaXRyYXJ5VmFsdWUsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIHRoZW1lQXNwZWN0XVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIENvbnRhaW5lclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2NvbnRhaW5lclxuICAgICAgICogQGRlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjAuMFxuICAgICAgICovXG4gICAgICBjb250YWluZXI6IFsnY29udGFpbmVyJ10sXG4gICAgICAvKipcbiAgICAgICAqIENvbnRhaW5lciBUeXBlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcmVzcG9uc2l2ZS1kZXNpZ24jY29udGFpbmVyLXF1ZXJpZXNcbiAgICAgICAqL1xuICAgICAgJ2NvbnRhaW5lci10eXBlJzogW3tcbiAgICAgICAgJ0Bjb250YWluZXInOiBbJycsICdub3JtYWwnLCAnc2l6ZScsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQ29udGFpbmVyIE5hbWVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9yZXNwb25zaXZlLWRlc2lnbiNuYW1lZC1jb250YWluZXJzXG4gICAgICAgKi9cbiAgICAgICdjb250YWluZXItbmFtZWQnOiBbaXNOYW1lZENvbnRhaW5lclF1ZXJ5XSxcbiAgICAgIC8qKlxuICAgICAgICogQ29sdW1uc1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2NvbHVtbnNcbiAgICAgICAqL1xuICAgICAgY29sdW1uczogW3tcbiAgICAgICAgY29sdW1uczogW2lzTnVtYmVyLCBpc0FyYml0cmFyeVZhbHVlLCBpc0FyYml0cmFyeVZhcmlhYmxlLCB0aGVtZUNvbnRhaW5lcl1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCcmVhayBBZnRlclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JyZWFrLWFmdGVyXG4gICAgICAgKi9cbiAgICAgICdicmVhay1hZnRlcic6IFt7XG4gICAgICAgICdicmVhay1hZnRlcic6IHNjYWxlQnJlYWsoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJyZWFrIEJlZm9yZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JyZWFrLWJlZm9yZVxuICAgICAgICovXG4gICAgICAnYnJlYWstYmVmb3JlJzogW3tcbiAgICAgICAgJ2JyZWFrLWJlZm9yZSc6IHNjYWxlQnJlYWsoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJyZWFrIEluc2lkZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JyZWFrLWluc2lkZVxuICAgICAgICovXG4gICAgICAnYnJlYWstaW5zaWRlJzogW3tcbiAgICAgICAgJ2JyZWFrLWluc2lkZSc6IFsnYXV0bycsICdhdm9pZCcsICdhdm9pZC1wYWdlJywgJ2F2b2lkLWNvbHVtbiddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm94IERlY29yYXRpb24gQnJlYWtcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3gtZGVjb3JhdGlvbi1icmVha1xuICAgICAgICovXG4gICAgICAnYm94LWRlY29yYXRpb24nOiBbe1xuICAgICAgICAnYm94LWRlY29yYXRpb24nOiBbJ3NsaWNlJywgJ2Nsb25lJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3ggU2l6aW5nXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm94LXNpemluZ1xuICAgICAgICovXG4gICAgICBib3g6IFt7XG4gICAgICAgIGJveDogWydib3JkZXInLCAnY29udGVudCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRGlzcGxheVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2Rpc3BsYXlcbiAgICAgICAqL1xuICAgICAgZGlzcGxheTogWydibG9jaycsICdpbmxpbmUtYmxvY2snLCAnaW5saW5lJywgJ2ZsZXgnLCAnaW5saW5lLWZsZXgnLCAndGFibGUnLCAnaW5saW5lLXRhYmxlJywgJ3RhYmxlLWNhcHRpb24nLCAndGFibGUtY2VsbCcsICd0YWJsZS1jb2x1bW4nLCAndGFibGUtY29sdW1uLWdyb3VwJywgJ3RhYmxlLWZvb3Rlci1ncm91cCcsICd0YWJsZS1oZWFkZXItZ3JvdXAnLCAndGFibGUtcm93LWdyb3VwJywgJ3RhYmxlLXJvdycsICdmbG93LXJvb3QnLCAnZ3JpZCcsICdpbmxpbmUtZ3JpZCcsICdjb250ZW50cycsICdsaXN0LWl0ZW0nLCAnaGlkZGVuJ10sXG4gICAgICAvKipcbiAgICAgICAqIFNjcmVlbiBSZWFkZXIgT25seVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2Rpc3BsYXkjc2NyZWVuLXJlYWRlci1vbmx5XG4gICAgICAgKi9cbiAgICAgIHNyOiBbJ3NyLW9ubHknLCAnbm90LXNyLW9ubHknXSxcbiAgICAgIC8qKlxuICAgICAgICogRmxvYXRzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZmxvYXRcbiAgICAgICAqL1xuICAgICAgZmxvYXQ6IFt7XG4gICAgICAgIGZsb2F0OiBbJ3JpZ2h0JywgJ2xlZnQnLCAnbm9uZScsICdzdGFydCcsICdlbmQnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIENsZWFyXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY2xlYXJcbiAgICAgICAqL1xuICAgICAgY2xlYXI6IFt7XG4gICAgICAgIGNsZWFyOiBbJ2xlZnQnLCAncmlnaHQnLCAnYm90aCcsICdub25lJywgJ3N0YXJ0JywgJ2VuZCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSXNvbGF0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvaXNvbGF0aW9uXG4gICAgICAgKi9cbiAgICAgIGlzb2xhdGlvbjogWydpc29sYXRlJywgJ2lzb2xhdGlvbi1hdXRvJ10sXG4gICAgICAvKipcbiAgICAgICAqIE9iamVjdCBGaXRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9vYmplY3QtZml0XG4gICAgICAgKi9cbiAgICAgICdvYmplY3QtZml0JzogW3tcbiAgICAgICAgb2JqZWN0OiBbJ2NvbnRhaW4nLCAnY292ZXInLCAnZmlsbCcsICdub25lJywgJ3NjYWxlLWRvd24nXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE9iamVjdCBQb3NpdGlvblxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL29iamVjdC1wb3NpdGlvblxuICAgICAgICovXG4gICAgICAnb2JqZWN0LXBvc2l0aW9uJzogW3tcbiAgICAgICAgb2JqZWN0OiBzY2FsZVBvc2l0aW9uV2l0aEFyYml0cmFyeSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3ZlcmZsb3dcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9vdmVyZmxvd1xuICAgICAgICovXG4gICAgICBvdmVyZmxvdzogW3tcbiAgICAgICAgb3ZlcmZsb3c6IHNjYWxlT3ZlcmZsb3coKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE92ZXJmbG93IFhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9vdmVyZmxvd1xuICAgICAgICovXG4gICAgICAnb3ZlcmZsb3cteCc6IFt7XG4gICAgICAgICdvdmVyZmxvdy14Jzogc2NhbGVPdmVyZmxvdygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3ZlcmZsb3cgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL292ZXJmbG93XG4gICAgICAgKi9cbiAgICAgICdvdmVyZmxvdy15JzogW3tcbiAgICAgICAgJ292ZXJmbG93LXknOiBzY2FsZU92ZXJmbG93KClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBPdmVyc2Nyb2xsIEJlaGF2aW9yXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvb3ZlcnNjcm9sbC1iZWhhdmlvclxuICAgICAgICovXG4gICAgICBvdmVyc2Nyb2xsOiBbe1xuICAgICAgICBvdmVyc2Nyb2xsOiBzY2FsZU92ZXJzY3JvbGwoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE92ZXJzY3JvbGwgQmVoYXZpb3IgWFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL292ZXJzY3JvbGwtYmVoYXZpb3JcbiAgICAgICAqL1xuICAgICAgJ292ZXJzY3JvbGwteCc6IFt7XG4gICAgICAgICdvdmVyc2Nyb2xsLXgnOiBzY2FsZU92ZXJzY3JvbGwoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE92ZXJzY3JvbGwgQmVoYXZpb3IgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL292ZXJzY3JvbGwtYmVoYXZpb3JcbiAgICAgICAqL1xuICAgICAgJ292ZXJzY3JvbGwteSc6IFt7XG4gICAgICAgICdvdmVyc2Nyb2xsLXknOiBzY2FsZU92ZXJzY3JvbGwoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBvc2l0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcG9zaXRpb25cbiAgICAgICAqL1xuICAgICAgcG9zaXRpb246IFsnc3RhdGljJywgJ2ZpeGVkJywgJ2Fic29sdXRlJywgJ3JlbGF0aXZlJywgJ3N0aWNreSddLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICBpbnNldDogW3tcbiAgICAgICAgaW5zZXQ6IHNjYWxlSW5zZXQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEluc2V0IElubGluZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICAnaW5zZXQteCc6IFt7XG4gICAgICAgICdpbnNldC14Jzogc2NhbGVJbnNldCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSW5zZXQgQmxvY2tcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90b3AtcmlnaHQtYm90dG9tLWxlZnRcbiAgICAgICAqL1xuICAgICAgJ2luc2V0LXknOiBbe1xuICAgICAgICAnaW5zZXQteSc6IHNjYWxlSW5zZXQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEluc2V0IElubGluZSBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICogQHRvZG8gY2xhc3MgZ3JvdXAgd2lsbCBiZSByZW5hbWVkIHRvIGBpbnNldC1zYCBpbiBuZXh0IG1ham9yIHJlbGVhc2VcbiAgICAgICAqL1xuICAgICAgc3RhcnQ6IFt7XG4gICAgICAgICdpbnNldC1zJzogc2NhbGVJbnNldCgpLFxuICAgICAgICAvKipcbiAgICAgICAgICogQGRlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjIuMCBpbiBmYXZvciBvZiBgaW5zZXQtcy0qYCB1dGlsaXRpZXMuXG4gICAgICAgICAqIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy9wdWxsLzE5NjEzXG4gICAgICAgICAqL1xuICAgICAgICBzdGFydDogc2NhbGVJbnNldCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSW5zZXQgSW5saW5lIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICogQHRvZG8gY2xhc3MgZ3JvdXAgd2lsbCBiZSByZW5hbWVkIHRvIGBpbnNldC1lYCBpbiBuZXh0IG1ham9yIHJlbGVhc2VcbiAgICAgICAqL1xuICAgICAgZW5kOiBbe1xuICAgICAgICAnaW5zZXQtZSc6IHNjYWxlSW5zZXQoKSxcbiAgICAgICAgLyoqXG4gICAgICAgICAqIEBkZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4yLjAgaW4gZmF2b3Igb2YgYGluc2V0LWUtKmAgdXRpbGl0aWVzLlxuICAgICAgICAgKiBAc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS90YWlsd2luZGxhYnMvdGFpbHdpbmRjc3MvcHVsbC8xOTYxM1xuICAgICAgICAgKi9cbiAgICAgICAgZW5kOiBzY2FsZUluc2V0KClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldCBCbG9jayBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICAnaW5zZXQtYnMnOiBbe1xuICAgICAgICAnaW5zZXQtYnMnOiBzY2FsZUluc2V0KClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldCBCbG9jayBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90b3AtcmlnaHQtYm90dG9tLWxlZnRcbiAgICAgICAqL1xuICAgICAgJ2luc2V0LWJlJzogW3tcbiAgICAgICAgJ2luc2V0LWJlJzogc2NhbGVJbnNldCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVG9wXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdG9wLXJpZ2h0LWJvdHRvbS1sZWZ0XG4gICAgICAgKi9cbiAgICAgIHRvcDogW3tcbiAgICAgICAgdG9wOiBzY2FsZUluc2V0KClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBSaWdodFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICByaWdodDogW3tcbiAgICAgICAgcmlnaHQ6IHNjYWxlSW5zZXQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvdHRvbVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICBib3R0b206IFt7XG4gICAgICAgIGJvdHRvbTogc2NhbGVJbnNldCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTGVmdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvcC1yaWdodC1ib3R0b20tbGVmdFxuICAgICAgICovXG4gICAgICBsZWZ0OiBbe1xuICAgICAgICBsZWZ0OiBzY2FsZUluc2V0KClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBWaXNpYmlsaXR5XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdmlzaWJpbGl0eVxuICAgICAgICovXG4gICAgICB2aXNpYmlsaXR5OiBbJ3Zpc2libGUnLCAnaW52aXNpYmxlJywgJ2NvbGxhcHNlJ10sXG4gICAgICAvKipcbiAgICAgICAqIFotSW5kZXhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy96LWluZGV4XG4gICAgICAgKi9cbiAgICAgIHo6IFt7XG4gICAgICAgIHo6IFtpc0ludGVnZXIsICdhdXRvJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gRmxleGJveCBhbmQgR3JpZCAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBGbGV4IEJhc2lzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZmxleC1iYXNpc1xuICAgICAgICovXG4gICAgICBiYXNpczogW3tcbiAgICAgICAgYmFzaXM6IFtpc0ZyYWN0aW9uLCAnZnVsbCcsICdhdXRvJywgdGhlbWVDb250YWluZXIsIC4uLnNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKCldXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRmxleCBEaXJlY3Rpb25cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9mbGV4LWRpcmVjdGlvblxuICAgICAgICovXG4gICAgICAnZmxleC1kaXJlY3Rpb24nOiBbe1xuICAgICAgICBmbGV4OiBbJ3JvdycsICdyb3ctcmV2ZXJzZScsICdjb2wnLCAnY29sLXJldmVyc2UnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEZsZXggV3JhcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZsZXgtd3JhcFxuICAgICAgICovXG4gICAgICAnZmxleC13cmFwJzogW3tcbiAgICAgICAgZmxleDogWydub3dyYXAnLCAnd3JhcCcsICd3cmFwLXJldmVyc2UnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEZsZXhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9mbGV4XG4gICAgICAgKi9cbiAgICAgIGZsZXg6IFt7XG4gICAgICAgIGZsZXg6IFtpc051bWJlciwgaXNGcmFjdGlvbiwgJ2F1dG8nLCAnaW5pdGlhbCcsICdub25lJywgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGbGV4IEdyb3dcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9mbGV4LWdyb3dcbiAgICAgICAqL1xuICAgICAgZ3JvdzogW3tcbiAgICAgICAgZ3JvdzogWycnLCBpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGbGV4IFNocmlua1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZsZXgtc2hyaW5rXG4gICAgICAgKi9cbiAgICAgIHNocmluazogW3tcbiAgICAgICAgc2hyaW5rOiBbJycsIGlzTnVtYmVyLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE9yZGVyXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvb3JkZXJcbiAgICAgICAqL1xuICAgICAgb3JkZXI6IFt7XG4gICAgICAgIG9yZGVyOiBbaXNJbnRlZ2VyLCAnZmlyc3QnLCAnbGFzdCcsICdub25lJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmlkIFRlbXBsYXRlIENvbHVtbnNcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmlkLXRlbXBsYXRlLWNvbHVtbnNcbiAgICAgICAqL1xuICAgICAgJ2dyaWQtY29scyc6IFt7XG4gICAgICAgICdncmlkLWNvbHMnOiBzY2FsZUdyaWRUZW1wbGF0ZUNvbHNSb3dzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmlkIENvbHVtbiBTdGFydCAvIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyaWQtY29sdW1uXG4gICAgICAgKi9cbiAgICAgICdjb2wtc3RhcnQtZW5kJzogW3tcbiAgICAgICAgY29sOiBzY2FsZUdyaWRDb2xSb3dTdGFydEFuZEVuZCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogR3JpZCBDb2x1bW4gU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmlkLWNvbHVtblxuICAgICAgICovXG4gICAgICAnY29sLXN0YXJ0JzogW3tcbiAgICAgICAgJ2NvbC1zdGFydCc6IHNjYWxlR3JpZENvbFJvd1N0YXJ0T3JFbmQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdyaWQgQ29sdW1uIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyaWQtY29sdW1uXG4gICAgICAgKi9cbiAgICAgICdjb2wtZW5kJzogW3tcbiAgICAgICAgJ2NvbC1lbmQnOiBzY2FsZUdyaWRDb2xSb3dTdGFydE9yRW5kKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmlkIFRlbXBsYXRlIFJvd3NcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmlkLXRlbXBsYXRlLXJvd3NcbiAgICAgICAqL1xuICAgICAgJ2dyaWQtcm93cyc6IFt7XG4gICAgICAgICdncmlkLXJvd3MnOiBzY2FsZUdyaWRUZW1wbGF0ZUNvbHNSb3dzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmlkIFJvdyBTdGFydCAvIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyaWQtcm93XG4gICAgICAgKi9cbiAgICAgICdyb3ctc3RhcnQtZW5kJzogW3tcbiAgICAgICAgcm93OiBzY2FsZUdyaWRDb2xSb3dTdGFydEFuZEVuZCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogR3JpZCBSb3cgU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmlkLXJvd1xuICAgICAgICovXG4gICAgICAncm93LXN0YXJ0JzogW3tcbiAgICAgICAgJ3Jvdy1zdGFydCc6IHNjYWxlR3JpZENvbFJvd1N0YXJ0T3JFbmQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdyaWQgUm93IEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyaWQtcm93XG4gICAgICAgKi9cbiAgICAgICdyb3ctZW5kJzogW3tcbiAgICAgICAgJ3Jvdy1lbmQnOiBzY2FsZUdyaWRDb2xSb3dTdGFydE9yRW5kKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmlkIEF1dG8gRmxvd1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyaWQtYXV0by1mbG93XG4gICAgICAgKi9cbiAgICAgICdncmlkLWZsb3cnOiBbe1xuICAgICAgICAnZ3JpZC1mbG93JzogWydyb3cnLCAnY29sJywgJ2RlbnNlJywgJ3Jvdy1kZW5zZScsICdjb2wtZGVuc2UnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdyaWQgQXV0byBDb2x1bW5zXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JpZC1hdXRvLWNvbHVtbnNcbiAgICAgICAqL1xuICAgICAgJ2F1dG8tY29scyc6IFt7XG4gICAgICAgICdhdXRvLWNvbHMnOiBzY2FsZUdyaWRBdXRvQ29sc1Jvd3MoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdyaWQgQXV0byBSb3dzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JpZC1hdXRvLXJvd3NcbiAgICAgICAqL1xuICAgICAgJ2F1dG8tcm93cyc6IFt7XG4gICAgICAgICdhdXRvLXJvd3MnOiBzY2FsZUdyaWRBdXRvQ29sc1Jvd3MoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdhcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dhcFxuICAgICAgICovXG4gICAgICBnYXA6IFt7XG4gICAgICAgIGdhcDogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdhcCBYXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ2FwXG4gICAgICAgKi9cbiAgICAgICdnYXAteCc6IFt7XG4gICAgICAgICdnYXAteCc6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHYXAgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dhcFxuICAgICAgICovXG4gICAgICAnZ2FwLXknOiBbe1xuICAgICAgICAnZ2FwLXknOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSnVzdGlmeSBDb250ZW50XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvanVzdGlmeS1jb250ZW50XG4gICAgICAgKi9cbiAgICAgICdqdXN0aWZ5LWNvbnRlbnQnOiBbe1xuICAgICAgICBqdXN0aWZ5OiBbLi4uc2NhbGVBbGlnblByaW1hcnlBeGlzKCksICdub3JtYWwnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEp1c3RpZnkgSXRlbXNcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9qdXN0aWZ5LWl0ZW1zXG4gICAgICAgKi9cbiAgICAgICdqdXN0aWZ5LWl0ZW1zJzogW3tcbiAgICAgICAgJ2p1c3RpZnktaXRlbXMnOiBbLi4uc2NhbGVBbGlnblNlY29uZGFyeUF4aXMoKSwgJ25vcm1hbCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSnVzdGlmeSBTZWxmXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvanVzdGlmeS1zZWxmXG4gICAgICAgKi9cbiAgICAgICdqdXN0aWZ5LXNlbGYnOiBbe1xuICAgICAgICAnanVzdGlmeS1zZWxmJzogWydhdXRvJywgLi4uc2NhbGVBbGlnblNlY29uZGFyeUF4aXMoKV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBBbGlnbiBDb250ZW50XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYWxpZ24tY29udGVudFxuICAgICAgICovXG4gICAgICAnYWxpZ24tY29udGVudCc6IFt7XG4gICAgICAgIGNvbnRlbnQ6IFsnbm9ybWFsJywgLi4uc2NhbGVBbGlnblByaW1hcnlBeGlzKCldXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQWxpZ24gSXRlbXNcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9hbGlnbi1pdGVtc1xuICAgICAgICovXG4gICAgICAnYWxpZ24taXRlbXMnOiBbe1xuICAgICAgICBpdGVtczogWy4uLnNjYWxlQWxpZ25TZWNvbmRhcnlBeGlzKCksIHtcbiAgICAgICAgICBiYXNlbGluZTogWycnLCAnbGFzdCddXG4gICAgICAgIH1dXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQWxpZ24gU2VsZlxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2FsaWduLXNlbGZcbiAgICAgICAqL1xuICAgICAgJ2FsaWduLXNlbGYnOiBbe1xuICAgICAgICBzZWxmOiBbJ2F1dG8nLCAuLi5zY2FsZUFsaWduU2Vjb25kYXJ5QXhpcygpLCB7XG4gICAgICAgICAgYmFzZWxpbmU6IFsnJywgJ2xhc3QnXVxuICAgICAgICB9XVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBsYWNlIENvbnRlbnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9wbGFjZS1jb250ZW50XG4gICAgICAgKi9cbiAgICAgICdwbGFjZS1jb250ZW50JzogW3tcbiAgICAgICAgJ3BsYWNlLWNvbnRlbnQnOiBzY2FsZUFsaWduUHJpbWFyeUF4aXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBsYWNlIEl0ZW1zXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGxhY2UtaXRlbXNcbiAgICAgICAqL1xuICAgICAgJ3BsYWNlLWl0ZW1zJzogW3tcbiAgICAgICAgJ3BsYWNlLWl0ZW1zJzogWy4uLnNjYWxlQWxpZ25TZWNvbmRhcnlBeGlzKCksICdiYXNlbGluZSddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUGxhY2UgU2VsZlxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3BsYWNlLXNlbGZcbiAgICAgICAqL1xuICAgICAgJ3BsYWNlLXNlbGYnOiBbe1xuICAgICAgICAncGxhY2Utc2VsZic6IFsnYXV0bycsIC4uLnNjYWxlQWxpZ25TZWNvbmRhcnlBeGlzKCldXG4gICAgICB9XSxcbiAgICAgIC8vIFNwYWNpbmdcbiAgICAgIC8qKlxuICAgICAgICogUGFkZGluZ1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3BhZGRpbmdcbiAgICAgICAqL1xuICAgICAgcDogW3tcbiAgICAgICAgcDogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBhZGRpbmcgSW5saW5lXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBweDogW3tcbiAgICAgICAgcHg6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQYWRkaW5nIEJsb2NrXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBweTogW3tcbiAgICAgICAgcHk6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQYWRkaW5nIElubGluZSBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3BhZGRpbmdcbiAgICAgICAqL1xuICAgICAgcHM6IFt7XG4gICAgICAgIHBzOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUGFkZGluZyBJbmxpbmUgRW5kXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwZTogW3tcbiAgICAgICAgcGU6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQYWRkaW5nIEJsb2NrIFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwYnM6IFt7XG4gICAgICAgIHBiczogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBhZGRpbmcgQmxvY2sgRW5kXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwYmU6IFt7XG4gICAgICAgIHBiZTogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBhZGRpbmcgVG9wXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwdDogW3tcbiAgICAgICAgcHQ6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQYWRkaW5nIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwcjogW3tcbiAgICAgICAgcHI6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQYWRkaW5nIEJvdHRvbVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3BhZGRpbmdcbiAgICAgICAqL1xuICAgICAgcGI6IFt7XG4gICAgICAgIHBiOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUGFkZGluZyBMZWZ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGFkZGluZ1xuICAgICAgICovXG4gICAgICBwbDogW3tcbiAgICAgICAgcGw6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBNYXJnaW5cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbTogW3tcbiAgICAgICAgbTogc2NhbGVNYXJnaW4oKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hcmdpbiBJbmxpbmVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbXg6IFt7XG4gICAgICAgIG14OiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIEJsb2NrXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFyZ2luXG4gICAgICAgKi9cbiAgICAgIG15OiBbe1xuICAgICAgICBteTogc2NhbGVNYXJnaW4oKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hcmdpbiBJbmxpbmUgU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbXM6IFt7XG4gICAgICAgIG1zOiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIElubGluZSBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbWU6IFt7XG4gICAgICAgIG1lOiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIEJsb2NrIFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFyZ2luXG4gICAgICAgKi9cbiAgICAgIG1iczogW3tcbiAgICAgICAgbWJzOiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIEJsb2NrIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hcmdpblxuICAgICAgICovXG4gICAgICBtYmU6IFt7XG4gICAgICAgIG1iZTogc2NhbGVNYXJnaW4oKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hcmdpbiBUb3BcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbXQ6IFt7XG4gICAgICAgIG10OiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFyZ2luXG4gICAgICAgKi9cbiAgICAgIG1yOiBbe1xuICAgICAgICBtcjogc2NhbGVNYXJnaW4oKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hcmdpbiBCb3R0b21cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbWI6IFt7XG4gICAgICAgIG1iOiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWFyZ2luIExlZnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW5cbiAgICAgICAqL1xuICAgICAgbWw6IFt7XG4gICAgICAgIG1sOiBzY2FsZU1hcmdpbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU3BhY2UgQmV0d2VlbiBYXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFyZ2luI2FkZGluZy1zcGFjZS1iZXR3ZWVuLWNoaWxkcmVuXG4gICAgICAgKi9cbiAgICAgICdzcGFjZS14JzogW3tcbiAgICAgICAgJ3NwYWNlLXgnOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU3BhY2UgQmV0d2VlbiBYIFJldmVyc2VcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXJnaW4jYWRkaW5nLXNwYWNlLWJldHdlZW4tY2hpbGRyZW5cbiAgICAgICAqL1xuICAgICAgJ3NwYWNlLXgtcmV2ZXJzZSc6IFsnc3BhY2UteC1yZXZlcnNlJ10sXG4gICAgICAvKipcbiAgICAgICAqIFNwYWNlIEJldHdlZW4gWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hcmdpbiNhZGRpbmctc3BhY2UtYmV0d2Vlbi1jaGlsZHJlblxuICAgICAgICovXG4gICAgICAnc3BhY2UteSc6IFt7XG4gICAgICAgICdzcGFjZS15Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNwYWNlIEJldHdlZW4gWSBSZXZlcnNlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFyZ2luI2FkZGluZy1zcGFjZS1iZXR3ZWVuLWNoaWxkcmVuXG4gICAgICAgKi9cbiAgICAgICdzcGFjZS15LXJldmVyc2UnOiBbJ3NwYWNlLXktcmV2ZXJzZSddLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8vIC0tLSBTaXppbmcgLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBTaXplXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvd2lkdGgjc2V0dGluZy1ib3RoLXdpZHRoLWFuZC1oZWlnaHRcbiAgICAgICAqL1xuICAgICAgc2l6ZTogW3tcbiAgICAgICAgc2l6ZTogc2NhbGVTaXppbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIElubGluZSBTaXplXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvd2lkdGhcbiAgICAgICAqL1xuICAgICAgJ2lubGluZS1zaXplJzogW3tcbiAgICAgICAgaW5saW5lOiBbJ2F1dG8nLCAuLi5zY2FsZVNpemluZ0lubGluZSgpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1pbi1JbmxpbmUgU2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21pbi13aWR0aFxuICAgICAgICovXG4gICAgICAnbWluLWlubGluZS1zaXplJzogW3tcbiAgICAgICAgJ21pbi1pbmxpbmUnOiBbJ2F1dG8nLCAuLi5zY2FsZVNpemluZ0lubGluZSgpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1heC1JbmxpbmUgU2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21heC13aWR0aFxuICAgICAgICovXG4gICAgICAnbWF4LWlubGluZS1zaXplJzogW3tcbiAgICAgICAgJ21heC1pbmxpbmUnOiBbJ25vbmUnLCAuLi5zY2FsZVNpemluZ0lubGluZSgpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJsb2NrIFNpemVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9oZWlnaHRcbiAgICAgICAqL1xuICAgICAgJ2Jsb2NrLXNpemUnOiBbe1xuICAgICAgICBibG9jazogWydhdXRvJywgLi4uc2NhbGVTaXppbmdCbG9jaygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1pbi1CbG9jayBTaXplXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWluLWhlaWdodFxuICAgICAgICovXG4gICAgICAnbWluLWJsb2NrLXNpemUnOiBbe1xuICAgICAgICAnbWluLWJsb2NrJzogWydhdXRvJywgLi4uc2NhbGVTaXppbmdCbG9jaygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1heC1CbG9jayBTaXplXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWF4LWhlaWdodFxuICAgICAgICovXG4gICAgICAnbWF4LWJsb2NrLXNpemUnOiBbe1xuICAgICAgICAnbWF4LWJsb2NrJzogWydub25lJywgLi4uc2NhbGVTaXppbmdCbG9jaygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvd2lkdGhcbiAgICAgICAqL1xuICAgICAgdzogW3tcbiAgICAgICAgdzogW3RoZW1lQ29udGFpbmVyLCAnc2NyZWVuJywgLi4uc2NhbGVTaXppbmcoKV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBNaW4tV2lkdGhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9taW4td2lkdGhcbiAgICAgICAqL1xuICAgICAgJ21pbi13JzogW3tcbiAgICAgICAgJ21pbi13JzogW3RoZW1lQ29udGFpbmVyLCAnc2NyZWVuJywgLyoqIERlcHJlY2F0ZWQuIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy5jb20vaXNzdWVzLzIwMjcjaXNzdWVjb21tZW50LTI2MjAxNTI3NTcgKi9cbiAgICAgICAgJ25vbmUnLCAuLi5zY2FsZVNpemluZygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1heC1XaWR0aFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21heC13aWR0aFxuICAgICAgICovXG4gICAgICAnbWF4LXcnOiBbe1xuICAgICAgICAnbWF4LXcnOiBbdGhlbWVDb250YWluZXIsICdzY3JlZW4nLCAnbm9uZScsIC8qKiBEZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4wLjAuIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy5jb20vaXNzdWVzLzIwMjcjaXNzdWVjb21tZW50LTI2MjAxNTI3NTcgKi9cbiAgICAgICAgJ3Byb3NlJywgLyoqIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjAuMC4gQHNlZSBodHRwczovL2dpdGh1Yi5jb20vdGFpbHdpbmRsYWJzL3RhaWx3aW5kY3NzLmNvbS9pc3N1ZXMvMjAyNyNpc3N1ZWNvbW1lbnQtMjYyMDE1Mjc1NyAqL1xuICAgICAgICB7XG4gICAgICAgICAgc2NyZWVuOiBbdGhlbWVCcmVha3BvaW50XVxuICAgICAgICB9LCAuLi5zY2FsZVNpemluZygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEhlaWdodFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2hlaWdodFxuICAgICAgICovXG4gICAgICBoOiBbe1xuICAgICAgICBoOiBbJ3NjcmVlbicsICdsaCcsIC4uLnNjYWxlU2l6aW5nKCldXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWluLUhlaWdodFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21pbi1oZWlnaHRcbiAgICAgICAqL1xuICAgICAgJ21pbi1oJzogW3tcbiAgICAgICAgJ21pbi1oJzogWydzY3JlZW4nLCAnbGgnLCAnbm9uZScsIC4uLnNjYWxlU2l6aW5nKCldXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTWF4LUhlaWdodFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21heC1oZWlnaHRcbiAgICAgICAqL1xuICAgICAgJ21heC1oJzogW3tcbiAgICAgICAgJ21heC1oJzogWydzY3JlZW4nLCAnbGgnLCAuLi5zY2FsZVNpemluZygpXVxuICAgICAgfV0sXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8vIC0tLSBUeXBvZ3JhcGh5IC0tLVxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvKipcbiAgICAgICAqIEZvbnQgU2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtc2l6ZVxuICAgICAgICovXG4gICAgICAnZm9udC1zaXplJzogW3tcbiAgICAgICAgdGV4dDogWydiYXNlJywgdGhlbWVUZXh0LCBpc0FyYml0cmFyeVZhcmlhYmxlTGVuZ3RoLCBpc0FyYml0cmFyeUxlbmd0aF1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IFNtb290aGluZ1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtc21vb3RoaW5nXG4gICAgICAgKi9cbiAgICAgICdmb250LXNtb290aGluZyc6IFsnYW50aWFsaWFzZWQnLCAnc3VicGl4ZWwtYW50aWFsaWFzZWQnXSxcbiAgICAgIC8qKlxuICAgICAgICogRm9udCBTdHlsZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtc3R5bGVcbiAgICAgICAqL1xuICAgICAgJ2ZvbnQtc3R5bGUnOiBbJ2l0YWxpYycsICdub3QtaXRhbGljJ10sXG4gICAgICAvKipcbiAgICAgICAqIEZvbnQgV2VpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZm9udC13ZWlnaHRcbiAgICAgICAqL1xuICAgICAgJ2ZvbnQtd2VpZ2h0JzogW3tcbiAgICAgICAgZm9udDogW3RoZW1lRm9udFdlaWdodCwgaXNBcmJpdHJhcnlWYXJpYWJsZVdlaWdodCwgaXNBcmJpdHJhcnlXZWlnaHRdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRm9udCBTdHJldGNoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZm9udC1zdHJldGNoXG4gICAgICAgKi9cbiAgICAgICdmb250LXN0cmV0Y2gnOiBbe1xuICAgICAgICAnZm9udC1zdHJldGNoJzogWyd1bHRyYS1jb25kZW5zZWQnLCAnZXh0cmEtY29uZGVuc2VkJywgJ2NvbmRlbnNlZCcsICdzZW1pLWNvbmRlbnNlZCcsICdub3JtYWwnLCAnc2VtaS1leHBhbmRlZCcsICdleHBhbmRlZCcsICdleHRyYS1leHBhbmRlZCcsICd1bHRyYS1leHBhbmRlZCcsIGlzUGVyY2VudCwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IEZhbWlseVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtZmFtaWx5XG4gICAgICAgKi9cbiAgICAgICdmb250LWZhbWlseSc6IFt7XG4gICAgICAgIGZvbnQ6IFtpc0FyYml0cmFyeVZhcmlhYmxlRmFtaWx5TmFtZSwgaXNBcmJpdHJhcnlGYW1pbHlOYW1lLCB0aGVtZUZvbnRdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRm9udCBGZWF0dXJlIFNldHRpbmdzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZm9udC1mZWF0dXJlLXNldHRpbmdzXG4gICAgICAgKi9cbiAgICAgICdmb250LWZlYXR1cmVzJzogW3tcbiAgICAgICAgJ2ZvbnQtZmVhdHVyZXMnOiBbaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IFZhcmlhbnQgTnVtZXJpY1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtdmFyaWFudC1udW1lcmljXG4gICAgICAgKi9cbiAgICAgICdmdm4tbm9ybWFsJzogWydub3JtYWwtbnVtcyddLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IFZhcmlhbnQgTnVtZXJpY1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtdmFyaWFudC1udW1lcmljXG4gICAgICAgKi9cbiAgICAgICdmdm4tb3JkaW5hbCc6IFsnb3JkaW5hbCddLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IFZhcmlhbnQgTnVtZXJpY1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtdmFyaWFudC1udW1lcmljXG4gICAgICAgKi9cbiAgICAgICdmdm4tc2xhc2hlZC16ZXJvJzogWydzbGFzaGVkLXplcm8nXSxcbiAgICAgIC8qKlxuICAgICAgICogRm9udCBWYXJpYW50IE51bWVyaWNcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9mb250LXZhcmlhbnQtbnVtZXJpY1xuICAgICAgICovXG4gICAgICAnZnZuLWZpZ3VyZSc6IFsnbGluaW5nLW51bXMnLCAnb2xkc3R5bGUtbnVtcyddLFxuICAgICAgLyoqXG4gICAgICAgKiBGb250IFZhcmlhbnQgTnVtZXJpY1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvbnQtdmFyaWFudC1udW1lcmljXG4gICAgICAgKi9cbiAgICAgICdmdm4tc3BhY2luZyc6IFsncHJvcG9ydGlvbmFsLW51bXMnLCAndGFidWxhci1udW1zJ10sXG4gICAgICAvKipcbiAgICAgICAqIEZvbnQgVmFyaWFudCBOdW1lcmljXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZm9udC12YXJpYW50LW51bWVyaWNcbiAgICAgICAqL1xuICAgICAgJ2Z2bi1mcmFjdGlvbic6IFsnZGlhZ29uYWwtZnJhY3Rpb25zJywgJ3N0YWNrZWQtZnJhY3Rpb25zJ10sXG4gICAgICAvKipcbiAgICAgICAqIExldHRlciBTcGFjaW5nXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbGV0dGVyLXNwYWNpbmdcbiAgICAgICAqL1xuICAgICAgdHJhY2tpbmc6IFt7XG4gICAgICAgIHRyYWNraW5nOiBbdGhlbWVUcmFja2luZywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBMaW5lIENsYW1wXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbGluZS1jbGFtcFxuICAgICAgICovXG4gICAgICAnbGluZS1jbGFtcCc6IFt7XG4gICAgICAgICdsaW5lLWNsYW1wJzogW2lzTnVtYmVyLCAnbm9uZScsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5TnVtYmVyXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIExpbmUgSGVpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbGluZS1oZWlnaHRcbiAgICAgICAqL1xuICAgICAgbGVhZGluZzogW3tcbiAgICAgICAgbGVhZGluZzogWy8qKiBEZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4wLjAuIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy5jb20vaXNzdWVzLzIwMjcjaXNzdWVjb21tZW50LTI2MjAxNTI3NTcgKi9cbiAgICAgICAgdGhlbWVMZWFkaW5nLCAuLi5zY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIExpc3QgU3R5bGUgSW1hZ2VcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9saXN0LXN0eWxlLWltYWdlXG4gICAgICAgKi9cbiAgICAgICdsaXN0LWltYWdlJzogW3tcbiAgICAgICAgJ2xpc3QtaW1hZ2UnOiBbJ25vbmUnLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIExpc3QgU3R5bGUgUG9zaXRpb25cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9saXN0LXN0eWxlLXBvc2l0aW9uXG4gICAgICAgKi9cbiAgICAgICdsaXN0LXN0eWxlLXBvc2l0aW9uJzogW3tcbiAgICAgICAgbGlzdDogWydpbnNpZGUnLCAnb3V0c2lkZSddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogTGlzdCBTdHlsZSBUeXBlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbGlzdC1zdHlsZS10eXBlXG4gICAgICAgKi9cbiAgICAgICdsaXN0LXN0eWxlLXR5cGUnOiBbe1xuICAgICAgICBsaXN0OiBbJ2Rpc2MnLCAnZGVjaW1hbCcsICdub25lJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IEFsaWdubWVudFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RleHQtYWxpZ25cbiAgICAgICAqL1xuICAgICAgJ3RleHQtYWxpZ25tZW50JzogW3tcbiAgICAgICAgdGV4dDogWydsZWZ0JywgJ2NlbnRlcicsICdyaWdodCcsICdqdXN0aWZ5JywgJ3N0YXJ0JywgJ2VuZCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUGxhY2Vob2xkZXIgQ29sb3JcbiAgICAgICAqIEBkZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2My4wLjBcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly92My50YWlsd2luZGNzcy5jb20vZG9jcy9wbGFjZWhvbGRlci1jb2xvclxuICAgICAgICovXG4gICAgICAncGxhY2Vob2xkZXItY29sb3InOiBbe1xuICAgICAgICBwbGFjZWhvbGRlcjogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVGV4dCBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RleHQtY29sb3JcbiAgICAgICAqL1xuICAgICAgJ3RleHQtY29sb3InOiBbe1xuICAgICAgICB0ZXh0OiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IERlY29yYXRpb25cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90ZXh0LWRlY29yYXRpb25cbiAgICAgICAqL1xuICAgICAgJ3RleHQtZGVjb3JhdGlvbic6IFsndW5kZXJsaW5lJywgJ292ZXJsaW5lJywgJ2xpbmUtdGhyb3VnaCcsICduby11bmRlcmxpbmUnXSxcbiAgICAgIC8qKlxuICAgICAgICogVGV4dCBEZWNvcmF0aW9uIFN0eWxlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdGV4dC1kZWNvcmF0aW9uLXN0eWxlXG4gICAgICAgKi9cbiAgICAgICd0ZXh0LWRlY29yYXRpb24tc3R5bGUnOiBbe1xuICAgICAgICBkZWNvcmF0aW9uOiBbLi4uc2NhbGVMaW5lU3R5bGUoKSwgJ3dhdnknXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRleHQgRGVjb3JhdGlvbiBUaGlja25lc3NcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90ZXh0LWRlY29yYXRpb24tdGhpY2tuZXNzXG4gICAgICAgKi9cbiAgICAgICd0ZXh0LWRlY29yYXRpb24tdGhpY2tuZXNzJzogW3tcbiAgICAgICAgZGVjb3JhdGlvbjogW2lzTnVtYmVyLCAnZnJvbS1mb250JywgJ2F1dG8nLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeUxlbmd0aF1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IERlY29yYXRpb24gQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90ZXh0LWRlY29yYXRpb24tY29sb3JcbiAgICAgICAqL1xuICAgICAgJ3RleHQtZGVjb3JhdGlvbi1jb2xvcic6IFt7XG4gICAgICAgIGRlY29yYXRpb246IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRleHQgVW5kZXJsaW5lIE9mZnNldFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RleHQtdW5kZXJsaW5lLW9mZnNldFxuICAgICAgICovXG4gICAgICAndW5kZXJsaW5lLW9mZnNldCc6IFt7XG4gICAgICAgICd1bmRlcmxpbmUtb2Zmc2V0JzogW2lzTnVtYmVyLCAnYXV0bycsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVGV4dCBUcmFuc2Zvcm1cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90ZXh0LXRyYW5zZm9ybVxuICAgICAgICovXG4gICAgICAndGV4dC10cmFuc2Zvcm0nOiBbJ3VwcGVyY2FzZScsICdsb3dlcmNhc2UnLCAnY2FwaXRhbGl6ZScsICdub3JtYWwtY2FzZSddLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IE92ZXJmbG93XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdGV4dC1vdmVyZmxvd1xuICAgICAgICovXG4gICAgICAndGV4dC1vdmVyZmxvdyc6IFsndHJ1bmNhdGUnLCAndGV4dC1lbGxpcHNpcycsICd0ZXh0LWNsaXAnXSxcbiAgICAgIC8qKlxuICAgICAgICogVGV4dCBXcmFwXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdGV4dC13cmFwXG4gICAgICAgKi9cbiAgICAgICd0ZXh0LXdyYXAnOiBbe1xuICAgICAgICB0ZXh0OiBbJ3dyYXAnLCAnbm93cmFwJywgJ2JhbGFuY2UnLCAncHJldHR5J11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IEluZGVudFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RleHQtaW5kZW50XG4gICAgICAgKi9cbiAgICAgIGluZGVudDogW3tcbiAgICAgICAgaW5kZW50OiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVGFiIFNpemVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90YWItc2l6ZVxuICAgICAgICovXG4gICAgICAndGFiLXNpemUnOiBbe1xuICAgICAgICB0YWI6IFtpc0ludGVnZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVmVydGljYWwgQWxpZ25tZW50XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdmVydGljYWwtYWxpZ25cbiAgICAgICAqL1xuICAgICAgJ3ZlcnRpY2FsLWFsaWduJzogW3tcbiAgICAgICAgYWxpZ246IFsnYmFzZWxpbmUnLCAndG9wJywgJ21pZGRsZScsICdib3R0b20nLCAndGV4dC10b3AnLCAndGV4dC1ib3R0b20nLCAnc3ViJywgJ3N1cGVyJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBXaGl0ZXNwYWNlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvd2hpdGVzcGFjZVxuICAgICAgICovXG4gICAgICB3aGl0ZXNwYWNlOiBbe1xuICAgICAgICB3aGl0ZXNwYWNlOiBbJ25vcm1hbCcsICdub3dyYXAnLCAncHJlJywgJ3ByZS1saW5lJywgJ3ByZS13cmFwJywgJ2JyZWFrLXNwYWNlcyddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogV29yZCBCcmVha1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3dvcmQtYnJlYWtcbiAgICAgICAqL1xuICAgICAgYnJlYWs6IFt7XG4gICAgICAgIGJyZWFrOiBbJ25vcm1hbCcsICd3b3JkcycsICdhbGwnLCAna2VlcCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3ZlcmZsb3cgV3JhcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL292ZXJmbG93LXdyYXBcbiAgICAgICAqL1xuICAgICAgd3JhcDogW3tcbiAgICAgICAgd3JhcDogWydicmVhay13b3JkJywgJ2FueXdoZXJlJywgJ25vcm1hbCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSHlwaGVuc1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2h5cGhlbnNcbiAgICAgICAqL1xuICAgICAgaHlwaGVuczogW3tcbiAgICAgICAgaHlwaGVuczogWydub25lJywgJ21hbnVhbCcsICdhdXRvJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBDb250ZW50XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY29udGVudFxuICAgICAgICovXG4gICAgICBjb250ZW50OiBbe1xuICAgICAgICBjb250ZW50OiBbJ25vbmUnLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gQmFja2dyb3VuZHMgLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tncm91bmQgQXR0YWNobWVudFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tncm91bmQtYXR0YWNobWVudFxuICAgICAgICovXG4gICAgICAnYmctYXR0YWNobWVudCc6IFt7XG4gICAgICAgIGJnOiBbJ2ZpeGVkJywgJ2xvY2FsJywgJ3Njcm9sbCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBDbGlwXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYmFja2dyb3VuZC1jbGlwXG4gICAgICAgKi9cbiAgICAgICdiZy1jbGlwJzogW3tcbiAgICAgICAgJ2JnLWNsaXAnOiBbJ2JvcmRlcicsICdwYWRkaW5nJywgJ2NvbnRlbnQnLCAndGV4dCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBPcmlnaW5cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZ3JvdW5kLW9yaWdpblxuICAgICAgICovXG4gICAgICAnYmctb3JpZ2luJzogW3tcbiAgICAgICAgJ2JnLW9yaWdpbic6IFsnYm9yZGVyJywgJ3BhZGRpbmcnLCAnY29udGVudCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBQb3NpdGlvblxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tncm91bmQtcG9zaXRpb25cbiAgICAgICAqL1xuICAgICAgJ2JnLXBvc2l0aW9uJzogW3tcbiAgICAgICAgYmc6IHNjYWxlQmdQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBSZXBlYXRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZ3JvdW5kLXJlcGVhdFxuICAgICAgICovXG4gICAgICAnYmctcmVwZWF0JzogW3tcbiAgICAgICAgYmc6IHNjYWxlQmdSZXBlYXQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tncm91bmQgU2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tncm91bmQtc2l6ZVxuICAgICAgICovXG4gICAgICAnYmctc2l6ZSc6IFt7XG4gICAgICAgIGJnOiBzY2FsZUJnU2l6ZSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBJbWFnZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tncm91bmQtaW1hZ2VcbiAgICAgICAqL1xuICAgICAgJ2JnLWltYWdlJzogW3tcbiAgICAgICAgYmc6IFsnbm9uZScsIHtcbiAgICAgICAgICBsaW5lYXI6IFt7XG4gICAgICAgICAgICB0bzogWyd0JywgJ3RyJywgJ3InLCAnYnInLCAnYicsICdibCcsICdsJywgJ3RsJ11cbiAgICAgICAgICB9LCBpc0ludGVnZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdLFxuICAgICAgICAgIHJhZGlhbDogWycnLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXSxcbiAgICAgICAgICBjb25pYzogW2lzSW50ZWdlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgICAgfSwgaXNBcmJpdHJhcnlWYXJpYWJsZUltYWdlLCBpc0FyYml0cmFyeUltYWdlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tncm91bmQgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZ3JvdW5kLWNvbG9yXG4gICAgICAgKi9cbiAgICAgICdiZy1jb2xvcic6IFt7XG4gICAgICAgIGJnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmFkaWVudCBDb2xvciBTdG9wcyBGcm9tIFBvc2l0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JhZGllbnQtY29sb3Itc3RvcHNcbiAgICAgICAqL1xuICAgICAgJ2dyYWRpZW50LWZyb20tcG9zJzogW3tcbiAgICAgICAgZnJvbTogc2NhbGVHcmFkaWVudFN0b3BQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogR3JhZGllbnQgQ29sb3IgU3RvcHMgVmlhIFBvc2l0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JhZGllbnQtY29sb3Itc3RvcHNcbiAgICAgICAqL1xuICAgICAgJ2dyYWRpZW50LXZpYS1wb3MnOiBbe1xuICAgICAgICB2aWE6IHNjYWxlR3JhZGllbnRTdG9wUG9zaXRpb24oKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEdyYWRpZW50IENvbG9yIFN0b3BzIFRvIFBvc2l0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JhZGllbnQtY29sb3Itc3RvcHNcbiAgICAgICAqL1xuICAgICAgJ2dyYWRpZW50LXRvLXBvcyc6IFt7XG4gICAgICAgIHRvOiBzY2FsZUdyYWRpZW50U3RvcFBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmFkaWVudCBDb2xvciBTdG9wcyBGcm9tXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZ3JhZGllbnQtY29sb3Itc3RvcHNcbiAgICAgICAqL1xuICAgICAgJ2dyYWRpZW50LWZyb20nOiBbe1xuICAgICAgICBmcm9tOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmFkaWVudCBDb2xvciBTdG9wcyBWaWFcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmFkaWVudC1jb2xvci1zdG9wc1xuICAgICAgICovXG4gICAgICAnZ3JhZGllbnQtdmlhJzogW3tcbiAgICAgICAgdmlhOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmFkaWVudCBDb2xvciBTdG9wcyBUb1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2dyYWRpZW50LWNvbG9yLXN0b3BzXG4gICAgICAgKi9cbiAgICAgICdncmFkaWVudC10byc6IFt7XG4gICAgICAgIHRvOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gQm9yZGVycyAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICByb3VuZGVkOiBbe1xuICAgICAgICByb3VuZGVkOiBzY2FsZVJhZGl1cygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFJhZGl1cyBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1yYWRpdXNcbiAgICAgICAqL1xuICAgICAgJ3JvdW5kZWQtcyc6IFt7XG4gICAgICAgICdyb3VuZGVkLXMnOiBzY2FsZVJhZGl1cygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFJhZGl1cyBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItcmFkaXVzXG4gICAgICAgKi9cbiAgICAgICdyb3VuZGVkLWUnOiBbe1xuICAgICAgICAncm91bmRlZC1lJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgVG9wXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC10JzogW3tcbiAgICAgICAgJ3JvdW5kZWQtdCc6IHNjYWxlUmFkaXVzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC1yJzogW3tcbiAgICAgICAgJ3JvdW5kZWQtcic6IHNjYWxlUmFkaXVzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzIEJvdHRvbVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1yYWRpdXNcbiAgICAgICAqL1xuICAgICAgJ3JvdW5kZWQtYic6IFt7XG4gICAgICAgICdyb3VuZGVkLWInOiBzY2FsZVJhZGl1cygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFJhZGl1cyBMZWZ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC1sJzogW3tcbiAgICAgICAgJ3JvdW5kZWQtbCc6IHNjYWxlUmFkaXVzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzIFN0YXJ0IFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC1zcyc6IFt7XG4gICAgICAgICdyb3VuZGVkLXNzJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgU3RhcnQgRW5kXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC1zZSc6IFt7XG4gICAgICAgICdyb3VuZGVkLXNlJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgRW5kIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1yYWRpdXNcbiAgICAgICAqL1xuICAgICAgJ3JvdW5kZWQtZWUnOiBbe1xuICAgICAgICAncm91bmRlZC1lZSc6IHNjYWxlUmFkaXVzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzIEVuZCBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1yYWRpdXNcbiAgICAgICAqL1xuICAgICAgJ3JvdW5kZWQtZXMnOiBbe1xuICAgICAgICAncm91bmRlZC1lcyc6IHNjYWxlUmFkaXVzKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgUmFkaXVzIFRvcCBMZWZ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC10bCc6IFt7XG4gICAgICAgICdyb3VuZGVkLXRsJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgVG9wIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC10cic6IFt7XG4gICAgICAgICdyb3VuZGVkLXRyJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgQm90dG9tIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXJhZGl1c1xuICAgICAgICovXG4gICAgICAncm91bmRlZC1icic6IFt7XG4gICAgICAgICdyb3VuZGVkLWJyJzogc2NhbGVSYWRpdXMoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBSYWRpdXMgQm90dG9tIExlZnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItcmFkaXVzXG4gICAgICAgKi9cbiAgICAgICdyb3VuZGVkLWJsJzogW3tcbiAgICAgICAgJ3JvdW5kZWQtYmwnOiBzY2FsZVJhZGl1cygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXdpZHRoXG4gICAgICAgKi9cbiAgICAgICdib3JkZXItdyc6IFt7XG4gICAgICAgIGJvcmRlcjogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFdpZHRoIElubGluZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXcteCc6IFt7XG4gICAgICAgICdib3JkZXIteCc6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBXaWR0aCBCbG9ja1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXcteSc6IFt7XG4gICAgICAgICdib3JkZXIteSc6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBXaWR0aCBJbmxpbmUgU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItd2lkdGhcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci13LXMnOiBbe1xuICAgICAgICAnYm9yZGVyLXMnOiBzY2FsZUJvcmRlcldpZHRoKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgV2lkdGggSW5saW5lIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctZSc6IFt7XG4gICAgICAgICdib3JkZXItZSc6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBXaWR0aCBCbG9jayBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctYnMnOiBbe1xuICAgICAgICAnYm9yZGVyLWJzJzogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFdpZHRoIEJsb2NrIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctYmUnOiBbe1xuICAgICAgICAnYm9yZGVyLWJlJzogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIFdpZHRoIFRvcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctdCc6IFt7XG4gICAgICAgICdib3JkZXItdCc6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBXaWR0aCBSaWdodFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctcic6IFt7XG4gICAgICAgICdib3JkZXItcic6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBXaWR0aCBCb3R0b21cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItd2lkdGhcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci13LWInOiBbe1xuICAgICAgICAnYm9yZGVyLWInOiBzY2FsZUJvcmRlcldpZHRoKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgV2lkdGggTGVmdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aFxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXctbCc6IFt7XG4gICAgICAgICdib3JkZXItbCc6IHNjYWxlQm9yZGVyV2lkdGgoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIERpdmlkZSBXaWR0aCBYXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXdpZHRoI2JldHdlZW4tY2hpbGRyZW5cbiAgICAgICAqL1xuICAgICAgJ2RpdmlkZS14JzogW3tcbiAgICAgICAgJ2RpdmlkZS14Jzogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRGl2aWRlIFdpZHRoIFggUmV2ZXJzZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aCNiZXR3ZWVuLWNoaWxkcmVuXG4gICAgICAgKi9cbiAgICAgICdkaXZpZGUteC1yZXZlcnNlJzogWydkaXZpZGUteC1yZXZlcnNlJ10sXG4gICAgICAvKipcbiAgICAgICAqIERpdmlkZSBXaWR0aCBZXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXdpZHRoI2JldHdlZW4tY2hpbGRyZW5cbiAgICAgICAqL1xuICAgICAgJ2RpdmlkZS15JzogW3tcbiAgICAgICAgJ2RpdmlkZS15Jzogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRGl2aWRlIFdpZHRoIFkgUmV2ZXJzZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci13aWR0aCNiZXR3ZWVuLWNoaWxkcmVuXG4gICAgICAgKi9cbiAgICAgICdkaXZpZGUteS1yZXZlcnNlJzogWydkaXZpZGUteS1yZXZlcnNlJ10sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBTdHlsZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1zdHlsZVxuICAgICAgICovXG4gICAgICAnYm9yZGVyLXN0eWxlJzogW3tcbiAgICAgICAgYm9yZGVyOiBbLi4uc2NhbGVMaW5lU3R5bGUoKSwgJ2hpZGRlbicsICdub25lJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBEaXZpZGUgU3R5bGVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItc3R5bGUjc2V0dGluZy10aGUtZGl2aWRlci1zdHlsZVxuICAgICAgICovXG4gICAgICAnZGl2aWRlLXN0eWxlJzogW3tcbiAgICAgICAgZGl2aWRlOiBbLi4uc2NhbGVMaW5lU3R5bGUoKSwgJ2hpZGRlbicsICdub25lJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci1jb2xvcic6IFt7XG4gICAgICAgIGJvcmRlcjogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIENvbG9yIElubGluZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLXgnOiBbe1xuICAgICAgICAnYm9yZGVyLXgnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgQmxvY2tcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci1jb2xvci15JzogW3tcbiAgICAgICAgJ2JvcmRlci15Jzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIENvbG9yIElubGluZSBTdGFydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLXMnOiBbe1xuICAgICAgICAnYm9yZGVyLXMnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgSW5saW5lIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLWUnOiBbe1xuICAgICAgICAnYm9yZGVyLWUnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgQmxvY2sgU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci1jb2xvci1icyc6IFt7XG4gICAgICAgICdib3JkZXItYnMnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgQmxvY2sgRW5kXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLWNvbG9yXG4gICAgICAgKi9cbiAgICAgICdib3JkZXItY29sb3ItYmUnOiBbe1xuICAgICAgICAnYm9yZGVyLWJlJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIENvbG9yIFRvcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLXQnOiBbe1xuICAgICAgICAnYm9yZGVyLXQnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgUmlnaHRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci1jb2xvci1yJzogW3tcbiAgICAgICAgJ2JvcmRlci1yJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIENvbG9yIEJvdHRvbVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLWInOiBbe1xuICAgICAgICAnYm9yZGVyLWInOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCb3JkZXIgQ29sb3IgTGVmdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JvcmRlci1jb2xvclxuICAgICAgICovXG4gICAgICAnYm9yZGVyLWNvbG9yLWwnOiBbe1xuICAgICAgICAnYm9yZGVyLWwnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBEaXZpZGUgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9kaXZpZGUtY29sb3JcbiAgICAgICAqL1xuICAgICAgJ2RpdmlkZS1jb2xvcic6IFt7XG4gICAgICAgIGRpdmlkZTogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3V0bGluZSBTdHlsZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL291dGxpbmUtc3R5bGVcbiAgICAgICAqL1xuICAgICAgJ291dGxpbmUtc3R5bGUnOiBbe1xuICAgICAgICBvdXRsaW5lOiBbLi4uc2NhbGVMaW5lU3R5bGUoKSwgJ25vbmUnLCAnaGlkZGVuJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBPdXRsaW5lIE9mZnNldFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL291dGxpbmUtb2Zmc2V0XG4gICAgICAgKi9cbiAgICAgICdvdXRsaW5lLW9mZnNldCc6IFt7XG4gICAgICAgICdvdXRsaW5lLW9mZnNldCc6IFtpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBPdXRsaW5lIFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvb3V0bGluZS13aWR0aFxuICAgICAgICovXG4gICAgICAnb3V0bGluZS13JzogW3tcbiAgICAgICAgb3V0bGluZTogWycnLCBpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZUxlbmd0aCwgaXNBcmJpdHJhcnlMZW5ndGhdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3V0bGluZSBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL291dGxpbmUtY29sb3JcbiAgICAgICAqL1xuICAgICAgJ291dGxpbmUtY29sb3InOiBbe1xuICAgICAgICBvdXRsaW5lOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gRWZmZWN0cyAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBCb3ggU2hhZG93XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm94LXNoYWRvd1xuICAgICAgICovXG4gICAgICBzaGFkb3c6IFt7XG4gICAgICAgIHNoYWRvdzogW1xuICAgICAgICAvLyBEZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4wLjBcbiAgICAgICAgJycsICdub25lJywgdGhlbWVTaGFkb3csIGlzQXJiaXRyYXJ5VmFyaWFibGVTaGFkb3csIGlzQXJiaXRyYXJ5U2hhZG93XVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJveCBTaGFkb3cgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3gtc2hhZG93I3NldHRpbmctdGhlLXNoYWRvdy1jb2xvclxuICAgICAgICovXG4gICAgICAnc2hhZG93LWNvbG9yJzogW3tcbiAgICAgICAgc2hhZG93OiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldCBCb3ggU2hhZG93XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm94LXNoYWRvdyNhZGRpbmctYW4taW5zZXQtc2hhZG93XG4gICAgICAgKi9cbiAgICAgICdpbnNldC1zaGFkb3cnOiBbe1xuICAgICAgICAnaW5zZXQtc2hhZG93JzogWydub25lJywgdGhlbWVJbnNldFNoYWRvdywgaXNBcmJpdHJhcnlWYXJpYWJsZVNoYWRvdywgaXNBcmJpdHJhcnlTaGFkb3ddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSW5zZXQgQm94IFNoYWRvdyBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JveC1zaGFkb3cjc2V0dGluZy10aGUtaW5zZXQtc2hhZG93LWNvbG9yXG4gICAgICAgKi9cbiAgICAgICdpbnNldC1zaGFkb3ctY29sb3InOiBbe1xuICAgICAgICAnaW5zZXQtc2hhZG93Jzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUmluZyBXaWR0aFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JveC1zaGFkb3cjYWRkaW5nLWEtcmluZ1xuICAgICAgICovXG4gICAgICAncmluZy13JzogW3tcbiAgICAgICAgcmluZzogc2NhbGVCb3JkZXJXaWR0aCgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUmluZyBXaWR0aCBJbnNldFxuICAgICAgICogQHNlZSBodHRwczovL3YzLnRhaWx3aW5kY3NzLmNvbS9kb2NzL3Jpbmctd2lkdGgjaW5zZXQtcmluZ3NcbiAgICAgICAqIEBkZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4wLjBcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy9ibG9iL3Y0LjAuMC9wYWNrYWdlcy90YWlsd2luZGNzcy9zcmMvdXRpbGl0aWVzLnRzI0w0MTU4XG4gICAgICAgKi9cbiAgICAgICdyaW5nLXctaW5zZXQnOiBbJ3JpbmctaW5zZXQnXSxcbiAgICAgIC8qKlxuICAgICAgICogUmluZyBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JveC1zaGFkb3cjc2V0dGluZy10aGUtcmluZy1jb2xvclxuICAgICAgICovXG4gICAgICAncmluZy1jb2xvcic6IFt7XG4gICAgICAgIHJpbmc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFJpbmcgT2Zmc2V0IFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdjMudGFpbHdpbmRjc3MuY29tL2RvY3MvcmluZy1vZmZzZXQtd2lkdGhcbiAgICAgICAqIEBkZXByZWNhdGVkIHNpbmNlIFRhaWx3aW5kIENTUyB2NC4wLjBcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3RhaWx3aW5kbGFicy90YWlsd2luZGNzcy9ibG9iL3Y0LjAuMC9wYWNrYWdlcy90YWlsd2luZGNzcy9zcmMvdXRpbGl0aWVzLnRzI0w0MTU4XG4gICAgICAgKi9cbiAgICAgICdyaW5nLW9mZnNldC13JzogW3tcbiAgICAgICAgJ3Jpbmctb2Zmc2V0JzogW2lzTnVtYmVyLCBpc0FyYml0cmFyeUxlbmd0aF1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBSaW5nIE9mZnNldCBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3YzLnRhaWx3aW5kY3NzLmNvbS9kb2NzL3Jpbmctb2Zmc2V0LWNvbG9yXG4gICAgICAgKiBAZGVwcmVjYXRlZCBzaW5jZSBUYWlsd2luZCBDU1MgdjQuMC4wXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS90YWlsd2luZGxhYnMvdGFpbHdpbmRjc3MvYmxvYi92NC4wLjAvcGFja2FnZXMvdGFpbHdpbmRjc3Mvc3JjL3V0aWxpdGllcy50cyNMNDE1OFxuICAgICAgICovXG4gICAgICAncmluZy1vZmZzZXQtY29sb3InOiBbe1xuICAgICAgICAncmluZy1vZmZzZXQnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldCBSaW5nIFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm94LXNoYWRvdyNhZGRpbmctYW4taW5zZXQtcmluZ1xuICAgICAgICovXG4gICAgICAnaW5zZXQtcmluZy13JzogW3tcbiAgICAgICAgJ2luc2V0LXJpbmcnOiBzY2FsZUJvcmRlcldpZHRoKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnNldCBSaW5nIENvbG9yXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm94LXNoYWRvdyNzZXR0aW5nLXRoZS1pbnNldC1yaW5nLWNvbG9yXG4gICAgICAgKi9cbiAgICAgICdpbnNldC1yaW5nLWNvbG9yJzogW3tcbiAgICAgICAgJ2luc2V0LXJpbmcnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUZXh0IFNoYWRvd1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RleHQtc2hhZG93XG4gICAgICAgKi9cbiAgICAgICd0ZXh0LXNoYWRvdyc6IFt7XG4gICAgICAgICd0ZXh0LXNoYWRvdyc6IFsnbm9uZScsIHRoZW1lVGV4dFNoYWRvdywgaXNBcmJpdHJhcnlWYXJpYWJsZVNoYWRvdywgaXNBcmJpdHJhcnlTaGFkb3ddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVGV4dCBTaGFkb3cgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90ZXh0LXNoYWRvdyNzZXR0aW5nLXRoZS1zaGFkb3ctY29sb3JcbiAgICAgICAqL1xuICAgICAgJ3RleHQtc2hhZG93LWNvbG9yJzogW3tcbiAgICAgICAgJ3RleHQtc2hhZG93Jzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogT3BhY2l0eVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL29wYWNpdHlcbiAgICAgICAqL1xuICAgICAgb3BhY2l0eTogW3tcbiAgICAgICAgb3BhY2l0eTogW2lzTnVtYmVyLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1peCBCbGVuZCBNb2RlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWl4LWJsZW5kLW1vZGVcbiAgICAgICAqL1xuICAgICAgJ21peC1ibGVuZCc6IFt7XG4gICAgICAgICdtaXgtYmxlbmQnOiBbLi4uc2NhbGVCbGVuZE1vZGUoKSwgJ3BsdXMtZGFya2VyJywgJ3BsdXMtbGlnaHRlciddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2dyb3VuZCBCbGVuZCBNb2RlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYmFja2dyb3VuZC1ibGVuZC1tb2RlXG4gICAgICAgKi9cbiAgICAgICdiZy1ibGVuZCc6IFt7XG4gICAgICAgICdiZy1ibGVuZCc6IHNjYWxlQmxlbmRNb2RlKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBNYXNrIENsaXBcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXNrLWNsaXBcbiAgICAgICAqL1xuICAgICAgJ21hc2stY2xpcCc6IFt7XG4gICAgICAgICdtYXNrLWNsaXAnOiBbJ2JvcmRlcicsICdwYWRkaW5nJywgJ2NvbnRlbnQnLCAnZmlsbCcsICdzdHJva2UnLCAndmlldyddXG4gICAgICB9LCAnbWFzay1uby1jbGlwJ10sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgQ29tcG9zaXRlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFzay1jb21wb3NpdGVcbiAgICAgICAqL1xuICAgICAgJ21hc2stY29tcG9zaXRlJzogW3tcbiAgICAgICAgbWFzazogWydhZGQnLCAnc3VidHJhY3QnLCAnaW50ZXJzZWN0JywgJ2V4Y2x1ZGUnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgSW1hZ2VcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXNrLWltYWdlXG4gICAgICAgKi9cbiAgICAgICdtYXNrLWltYWdlLWxpbmVhci1wb3MnOiBbe1xuICAgICAgICAnbWFzay1saW5lYXInOiBbaXNOdW1iZXJdXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLWxpbmVhci1mcm9tLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLWxpbmVhci1mcm9tJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLWxpbmVhci10by1wb3MnOiBbe1xuICAgICAgICAnbWFzay1saW5lYXItdG8nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtbGluZWFyLWZyb20tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1saW5lYXItZnJvbSc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1saW5lYXItdG8tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1saW5lYXItdG8nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtdC1mcm9tLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLXQtZnJvbSc6IHNjYWxlTWFza0ltYWdlUG9zaXRpb24oKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS10LXRvLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLXQtdG8nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtdC1mcm9tLWNvbG9yJzogW3tcbiAgICAgICAgJ21hc2stdC1mcm9tJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXQtdG8tY29sb3InOiBbe1xuICAgICAgICAnbWFzay10LXRvJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXItZnJvbS1wb3MnOiBbe1xuICAgICAgICAnbWFzay1yLWZyb20nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2Utci10by1wb3MnOiBbe1xuICAgICAgICAnbWFzay1yLXRvJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXItZnJvbS1jb2xvcic6IFt7XG4gICAgICAgICdtYXNrLXItZnJvbSc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1yLXRvLWNvbG9yJzogW3tcbiAgICAgICAgJ21hc2stci10byc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1iLWZyb20tcG9zJzogW3tcbiAgICAgICAgJ21hc2stYi1mcm9tJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLWItdG8tcG9zJzogW3tcbiAgICAgICAgJ21hc2stYi10byc6IHNjYWxlTWFza0ltYWdlUG9zaXRpb24oKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1iLWZyb20tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1iLWZyb20nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtYi10by1jb2xvcic6IFt7XG4gICAgICAgICdtYXNrLWItdG8nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtbC1mcm9tLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLWwtZnJvbSc6IHNjYWxlTWFza0ltYWdlUG9zaXRpb24oKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1sLXRvLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLWwtdG8nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtbC1mcm9tLWNvbG9yJzogW3tcbiAgICAgICAgJ21hc2stbC1mcm9tJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLWwtdG8tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1sLXRvJzogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXgtZnJvbS1wb3MnOiBbe1xuICAgICAgICAnbWFzay14LWZyb20nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UteC10by1wb3MnOiBbe1xuICAgICAgICAnbWFzay14LXRvJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXgtZnJvbS1jb2xvcic6IFt7XG4gICAgICAgICdtYXNrLXgtZnJvbSc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS14LXRvLWNvbG9yJzogW3tcbiAgICAgICAgJ21hc2steC10byc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS15LWZyb20tcG9zJzogW3tcbiAgICAgICAgJ21hc2steS1mcm9tJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXktdG8tcG9zJzogW3tcbiAgICAgICAgJ21hc2steS10byc6IHNjYWxlTWFza0ltYWdlUG9zaXRpb24oKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS15LWZyb20tY29sb3InOiBbe1xuICAgICAgICAnbWFzay15LWZyb20nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UteS10by1jb2xvcic6IFt7XG4gICAgICAgICdtYXNrLXktdG8nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtcmFkaWFsJzogW3tcbiAgICAgICAgJ21hc2stcmFkaWFsJzogW2lzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXJhZGlhbC1mcm9tLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLXJhZGlhbC1mcm9tJzogc2NhbGVNYXNrSW1hZ2VQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXJhZGlhbC10by1wb3MnOiBbe1xuICAgICAgICAnbWFzay1yYWRpYWwtdG8nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtcmFkaWFsLWZyb20tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1yYWRpYWwtZnJvbSc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1yYWRpYWwtdG8tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1yYWRpYWwtdG8nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtcmFkaWFsLXNoYXBlJzogW3tcbiAgICAgICAgJ21hc2stcmFkaWFsJzogWydjaXJjbGUnLCAnZWxsaXBzZSddXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLXJhZGlhbC1zaXplJzogW3tcbiAgICAgICAgJ21hc2stcmFkaWFsJzogW3tcbiAgICAgICAgICBjbG9zZXN0OiBbJ3NpZGUnLCAnY29ybmVyJ10sXG4gICAgICAgICAgZmFydGhlc3Q6IFsnc2lkZScsICdjb3JuZXInXVxuICAgICAgICB9XVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1yYWRpYWwtcG9zJzogW3tcbiAgICAgICAgJ21hc2stcmFkaWFsLWF0Jzogc2NhbGVQb3NpdGlvbigpXG4gICAgICB9XSxcbiAgICAgICdtYXNrLWltYWdlLWNvbmljLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLWNvbmljJzogW2lzTnVtYmVyXVxuICAgICAgfV0sXG4gICAgICAnbWFzay1pbWFnZS1jb25pYy1mcm9tLXBvcyc6IFt7XG4gICAgICAgICdtYXNrLWNvbmljLWZyb20nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtY29uaWMtdG8tcG9zJzogW3tcbiAgICAgICAgJ21hc2stY29uaWMtdG8nOiBzY2FsZU1hc2tJbWFnZVBvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtY29uaWMtZnJvbS1jb2xvcic6IFt7XG4gICAgICAgICdtYXNrLWNvbmljLWZyb20nOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgJ21hc2staW1hZ2UtY29uaWMtdG8tY29sb3InOiBbe1xuICAgICAgICAnbWFzay1jb25pYy10byc6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgTW9kZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hc2stbW9kZVxuICAgICAgICovXG4gICAgICAnbWFzay1tb2RlJzogW3tcbiAgICAgICAgbWFzazogWydhbHBoYScsICdsdW1pbmFuY2UnLCAnbWF0Y2gnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgT3JpZ2luXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFzay1vcmlnaW5cbiAgICAgICAqL1xuICAgICAgJ21hc2stb3JpZ2luJzogW3tcbiAgICAgICAgJ21hc2stb3JpZ2luJzogWydib3JkZXInLCAncGFkZGluZycsICdjb250ZW50JywgJ2ZpbGwnLCAnc3Ryb2tlJywgJ3ZpZXcnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgUG9zaXRpb25cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9tYXNrLXBvc2l0aW9uXG4gICAgICAgKi9cbiAgICAgICdtYXNrLXBvc2l0aW9uJzogW3tcbiAgICAgICAgbWFzazogc2NhbGVCZ1Bvc2l0aW9uKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBNYXNrIFJlcGVhdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hc2stcmVwZWF0XG4gICAgICAgKi9cbiAgICAgICdtYXNrLXJlcGVhdCc6IFt7XG4gICAgICAgIG1hc2s6IHNjYWxlQmdSZXBlYXQoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgU2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hc2stc2l6ZVxuICAgICAgICovXG4gICAgICAnbWFzay1zaXplJzogW3tcbiAgICAgICAgbWFzazogc2NhbGVCZ1NpemUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIE1hc2sgVHlwZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL21hc2stdHlwZVxuICAgICAgICovXG4gICAgICAnbWFzay10eXBlJzogW3tcbiAgICAgICAgJ21hc2stdHlwZSc6IFsnYWxwaGEnLCAnbHVtaW5hbmNlJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBNYXNrIEltYWdlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvbWFzay1pbWFnZVxuICAgICAgICovXG4gICAgICAnbWFzay1pbWFnZSc6IFt7XG4gICAgICAgIG1hc2s6IFsnbm9uZScsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLVxuICAgICAgLy8gLS0tIEZpbHRlcnMgLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8qKlxuICAgICAgICogRmlsdGVyXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZmlsdGVyXG4gICAgICAgKi9cbiAgICAgIGZpbHRlcjogW3tcbiAgICAgICAgZmlsdGVyOiBbXG4gICAgICAgIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHYzLjAuMFxuICAgICAgICAnJywgJ25vbmUnLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJsdXJcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ibHVyXG4gICAgICAgKi9cbiAgICAgIGJsdXI6IFt7XG4gICAgICAgIGJsdXI6IHNjYWxlQmx1cigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQnJpZ2h0bmVzc1xuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JyaWdodG5lc3NcbiAgICAgICAqL1xuICAgICAgYnJpZ2h0bmVzczogW3tcbiAgICAgICAgYnJpZ2h0bmVzczogW2lzTnVtYmVyLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIENvbnRyYXN0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY29udHJhc3RcbiAgICAgICAqL1xuICAgICAgY29udHJhc3Q6IFt7XG4gICAgICAgIGNvbnRyYXN0OiBbaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogRHJvcCBTaGFkb3dcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9kcm9wLXNoYWRvd1xuICAgICAgICovXG4gICAgICAnZHJvcC1zaGFkb3cnOiBbe1xuICAgICAgICAnZHJvcC1zaGFkb3cnOiBbXG4gICAgICAgIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHY0LjAuMFxuICAgICAgICAnJywgJ25vbmUnLCB0aGVtZURyb3BTaGFkb3csIGlzQXJiaXRyYXJ5VmFyaWFibGVTaGFkb3csIGlzQXJiaXRyYXJ5U2hhZG93XVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIERyb3AgU2hhZG93IENvbG9yXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZmlsdGVyLWRyb3Atc2hhZG93I3NldHRpbmctdGhlLXNoYWRvdy1jb2xvclxuICAgICAgICovXG4gICAgICAnZHJvcC1zaGFkb3ctY29sb3InOiBbe1xuICAgICAgICAnZHJvcC1zaGFkb3cnOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBHcmF5c2NhbGVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ncmF5c2NhbGVcbiAgICAgICAqL1xuICAgICAgZ3JheXNjYWxlOiBbe1xuICAgICAgICBncmF5c2NhbGU6IFsnJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogSHVlIFJvdGF0ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2h1ZS1yb3RhdGVcbiAgICAgICAqL1xuICAgICAgJ2h1ZS1yb3RhdGUnOiBbe1xuICAgICAgICAnaHVlLXJvdGF0ZSc6IFtpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBJbnZlcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9pbnZlcnRcbiAgICAgICAqL1xuICAgICAgaW52ZXJ0OiBbe1xuICAgICAgICBpbnZlcnQ6IFsnJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2F0dXJhdGVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zYXR1cmF0ZVxuICAgICAgICovXG4gICAgICBzYXR1cmF0ZTogW3tcbiAgICAgICAgc2F0dXJhdGU6IFtpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTZXBpYVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3NlcGlhXG4gICAgICAgKi9cbiAgICAgIHNlcGlhOiBbe1xuICAgICAgICBzZXBpYTogWycnLCBpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCYWNrZHJvcCBGaWx0ZXJcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZHJvcC1maWx0ZXJcbiAgICAgICAqL1xuICAgICAgJ2JhY2tkcm9wLWZpbHRlcic6IFt7XG4gICAgICAgICdiYWNrZHJvcC1maWx0ZXInOiBbXG4gICAgICAgIC8vIERlcHJlY2F0ZWQgc2luY2UgVGFpbHdpbmQgQ1NTIHYzLjAuMFxuICAgICAgICAnJywgJ25vbmUnLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tkcm9wIEJsdXJcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZHJvcC1ibHVyXG4gICAgICAgKi9cbiAgICAgICdiYWNrZHJvcC1ibHVyJzogW3tcbiAgICAgICAgJ2JhY2tkcm9wLWJsdXInOiBzY2FsZUJsdXIoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tkcm9wIEJyaWdodG5lc3NcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZHJvcC1icmlnaHRuZXNzXG4gICAgICAgKi9cbiAgICAgICdiYWNrZHJvcC1icmlnaHRuZXNzJzogW3tcbiAgICAgICAgJ2JhY2tkcm9wLWJyaWdodG5lc3MnOiBbaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2Ryb3AgQ29udHJhc3RcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9iYWNrZHJvcC1jb250cmFzdFxuICAgICAgICovXG4gICAgICAnYmFja2Ryb3AtY29udHJhc3QnOiBbe1xuICAgICAgICAnYmFja2Ryb3AtY29udHJhc3QnOiBbaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2Ryb3AgR3JheXNjYWxlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYmFja2Ryb3AtZ3JheXNjYWxlXG4gICAgICAgKi9cbiAgICAgICdiYWNrZHJvcC1ncmF5c2NhbGUnOiBbe1xuICAgICAgICAnYmFja2Ryb3AtZ3JheXNjYWxlJzogWycnLCBpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCYWNrZHJvcCBIdWUgUm90YXRlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYmFja2Ryb3AtaHVlLXJvdGF0ZVxuICAgICAgICovXG4gICAgICAnYmFja2Ryb3AtaHVlLXJvdGF0ZSc6IFt7XG4gICAgICAgICdiYWNrZHJvcC1odWUtcm90YXRlJzogW2lzTnVtYmVyLCBpc0FyYml0cmFyeVZhcmlhYmxlLCBpc0FyYml0cmFyeVZhbHVlXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJhY2tkcm9wIEludmVydFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tkcm9wLWludmVydFxuICAgICAgICovXG4gICAgICAnYmFja2Ryb3AtaW52ZXJ0JzogW3tcbiAgICAgICAgJ2JhY2tkcm9wLWludmVydCc6IFsnJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQmFja2Ryb3AgT3BhY2l0eVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tkcm9wLW9wYWNpdHlcbiAgICAgICAqL1xuICAgICAgJ2JhY2tkcm9wLW9wYWNpdHknOiBbe1xuICAgICAgICAnYmFja2Ryb3Atb3BhY2l0eSc6IFtpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCYWNrZHJvcCBTYXR1cmF0ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tkcm9wLXNhdHVyYXRlXG4gICAgICAgKi9cbiAgICAgICdiYWNrZHJvcC1zYXR1cmF0ZSc6IFt7XG4gICAgICAgICdiYWNrZHJvcC1zYXR1cmF0ZSc6IFtpc051bWJlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBCYWNrZHJvcCBTZXBpYVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2JhY2tkcm9wLXNlcGlhXG4gICAgICAgKi9cbiAgICAgICdiYWNrZHJvcC1zZXBpYSc6IFt7XG4gICAgICAgICdiYWNrZHJvcC1zZXBpYSc6IFsnJywgaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gVGFibGVzIC0tLVxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8qKlxuICAgICAgICogQm9yZGVyIENvbGxhcHNlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLWNvbGxhcHNlXG4gICAgICAgKi9cbiAgICAgICdib3JkZXItY29sbGFwc2UnOiBbe1xuICAgICAgICBib3JkZXI6IFsnY29sbGFwc2UnLCAnc2VwYXJhdGUnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBTcGFjaW5nXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYm9yZGVyLXNwYWNpbmdcbiAgICAgICAqL1xuICAgICAgJ2JvcmRlci1zcGFjaW5nJzogW3tcbiAgICAgICAgJ2JvcmRlci1zcGFjaW5nJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBTcGFjaW5nIFhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItc3BhY2luZ1xuICAgICAgICovXG4gICAgICAnYm9yZGVyLXNwYWNpbmcteCc6IFt7XG4gICAgICAgICdib3JkZXItc3BhY2luZy14Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEJvcmRlciBTcGFjaW5nIFlcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9ib3JkZXItc3BhY2luZ1xuICAgICAgICovXG4gICAgICAnYm9yZGVyLXNwYWNpbmcteSc6IFt7XG4gICAgICAgICdib3JkZXItc3BhY2luZy15Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRhYmxlIExheW91dFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RhYmxlLWxheW91dFxuICAgICAgICovXG4gICAgICAndGFibGUtbGF5b3V0JzogW3tcbiAgICAgICAgdGFibGU6IFsnYXV0bycsICdmaXhlZCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQ2FwdGlvbiBTaWRlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY2FwdGlvbi1zaWRlXG4gICAgICAgKi9cbiAgICAgIGNhcHRpb246IFt7XG4gICAgICAgIGNhcHRpb246IFsndG9wJywgJ2JvdHRvbSddXG4gICAgICB9XSxcbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICAgICAgLy8gLS0tIFRyYW5zaXRpb25zIGFuZCBBbmltYXRpb24gLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8qKlxuICAgICAgICogVHJhbnNpdGlvbiBQcm9wZXJ0eVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zaXRpb24tcHJvcGVydHlcbiAgICAgICAqL1xuICAgICAgdHJhbnNpdGlvbjogW3tcbiAgICAgICAgdHJhbnNpdGlvbjogWycnLCAnYWxsJywgJ2NvbG9ycycsICdvcGFjaXR5JywgJ3NoYWRvdycsICd0cmFuc2Zvcm0nLCAnbm9uZScsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVHJhbnNpdGlvbiBCZWhhdmlvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zaXRpb24tYmVoYXZpb3JcbiAgICAgICAqL1xuICAgICAgJ3RyYW5zaXRpb24tYmVoYXZpb3InOiBbe1xuICAgICAgICB0cmFuc2l0aW9uOiBbJ25vcm1hbCcsICdkaXNjcmV0ZSddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVHJhbnNpdGlvbiBEdXJhdGlvblxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zaXRpb24tZHVyYXRpb25cbiAgICAgICAqL1xuICAgICAgZHVyYXRpb246IFt7XG4gICAgICAgIGR1cmF0aW9uOiBbaXNOdW1iZXIsICdpbml0aWFsJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUcmFuc2l0aW9uIFRpbWluZyBGdW5jdGlvblxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zaXRpb24tdGltaW5nLWZ1bmN0aW9uXG4gICAgICAgKi9cbiAgICAgIGVhc2U6IFt7XG4gICAgICAgIGVhc2U6IFsnbGluZWFyJywgJ2luaXRpYWwnLCB0aGVtZUVhc2UsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVHJhbnNpdGlvbiBEZWxheVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zaXRpb24tZGVsYXlcbiAgICAgICAqL1xuICAgICAgZGVsYXk6IFt7XG4gICAgICAgIGRlbGF5OiBbaXNOdW1iZXIsIGlzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWVdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQW5pbWF0aW9uXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYW5pbWF0aW9uXG4gICAgICAgKi9cbiAgICAgIGFuaW1hdGU6IFt7XG4gICAgICAgIGFuaW1hdGU6IFsnbm9uZScsIHRoZW1lQW5pbWF0ZSwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gVHJhbnNmb3JtcyAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBCYWNrZmFjZSBWaXNpYmlsaXR5XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvYmFja2ZhY2UtdmlzaWJpbGl0eVxuICAgICAgICovXG4gICAgICBiYWNrZmFjZTogW3tcbiAgICAgICAgYmFja2ZhY2U6IFsnaGlkZGVuJywgJ3Zpc2libGUnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBlcnNwZWN0aXZlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcGVyc3BlY3RpdmVcbiAgICAgICAqL1xuICAgICAgcGVyc3BlY3RpdmU6IFt7XG4gICAgICAgIHBlcnNwZWN0aXZlOiBbdGhlbWVQZXJzcGVjdGl2ZSwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBQZXJzcGVjdGl2ZSBPcmlnaW5cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9wZXJzcGVjdGl2ZS1vcmlnaW5cbiAgICAgICAqL1xuICAgICAgJ3BlcnNwZWN0aXZlLW9yaWdpbic6IFt7XG4gICAgICAgICdwZXJzcGVjdGl2ZS1vcmlnaW4nOiBzY2FsZVBvc2l0aW9uV2l0aEFyYml0cmFyeSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUm90YXRlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvcm90YXRlXG4gICAgICAgKi9cbiAgICAgIHJvdGF0ZTogW3tcbiAgICAgICAgcm90YXRlOiBzY2FsZVJvdGF0ZSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogUm90YXRlIFhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9yb3RhdGVcbiAgICAgICAqL1xuICAgICAgJ3JvdGF0ZS14JzogW3tcbiAgICAgICAgJ3JvdGF0ZS14Jzogc2NhbGVSb3RhdGUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFJvdGF0ZSBZXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvcm90YXRlXG4gICAgICAgKi9cbiAgICAgICdyb3RhdGUteSc6IFt7XG4gICAgICAgICdyb3RhdGUteSc6IHNjYWxlUm90YXRlKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBSb3RhdGUgWlxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3JvdGF0ZVxuICAgICAgICovXG4gICAgICAncm90YXRlLXonOiBbe1xuICAgICAgICAncm90YXRlLXonOiBzY2FsZVJvdGF0ZSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2NhbGVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY2FsZVxuICAgICAgICovXG4gICAgICBzY2FsZTogW3tcbiAgICAgICAgc2NhbGU6IHNjYWxlU2NhbGUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjYWxlIFhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY2FsZVxuICAgICAgICovXG4gICAgICAnc2NhbGUteCc6IFt7XG4gICAgICAgICdzY2FsZS14Jzogc2NhbGVTY2FsZSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2NhbGUgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3NjYWxlXG4gICAgICAgKi9cbiAgICAgICdzY2FsZS15JzogW3tcbiAgICAgICAgJ3NjYWxlLXknOiBzY2FsZVNjYWxlKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY2FsZSBaXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2NhbGVcbiAgICAgICAqL1xuICAgICAgJ3NjYWxlLXonOiBbe1xuICAgICAgICAnc2NhbGUteic6IHNjYWxlU2NhbGUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjYWxlIDNEXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2NhbGVcbiAgICAgICAqL1xuICAgICAgJ3NjYWxlLTNkJzogWydzY2FsZS0zZCddLFxuICAgICAgLyoqXG4gICAgICAgKiBTa2V3XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2tld1xuICAgICAgICovXG4gICAgICBza2V3OiBbe1xuICAgICAgICBza2V3OiBzY2FsZVNrZXcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNrZXcgWFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3NrZXdcbiAgICAgICAqL1xuICAgICAgJ3NrZXcteCc6IFt7XG4gICAgICAgICdza2V3LXgnOiBzY2FsZVNrZXcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNrZXcgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3NrZXdcbiAgICAgICAqL1xuICAgICAgJ3NrZXcteSc6IFt7XG4gICAgICAgICdza2V3LXknOiBzY2FsZVNrZXcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRyYW5zZm9ybVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zZm9ybVxuICAgICAgICovXG4gICAgICB0cmFuc2Zvcm06IFt7XG4gICAgICAgIHRyYW5zZm9ybTogW2lzQXJiaXRyYXJ5VmFyaWFibGUsIGlzQXJiaXRyYXJ5VmFsdWUsICcnLCAnbm9uZScsICdncHUnLCAnY3B1J11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUcmFuc2Zvcm0gT3JpZ2luXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdHJhbnNmb3JtLW9yaWdpblxuICAgICAgICovXG4gICAgICAndHJhbnNmb3JtLW9yaWdpbic6IFt7XG4gICAgICAgIG9yaWdpbjogc2NhbGVQb3NpdGlvbldpdGhBcmJpdHJhcnkoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRyYW5zZm9ybSBTdHlsZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zZm9ybS1zdHlsZVxuICAgICAgICovXG4gICAgICAndHJhbnNmb3JtLXN0eWxlJzogW3tcbiAgICAgICAgdHJhbnNmb3JtOiBbJzNkJywgJ2ZsYXQnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRyYW5zbGF0ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zbGF0ZVxuICAgICAgICovXG4gICAgICB0cmFuc2xhdGU6IFt7XG4gICAgICAgIHRyYW5zbGF0ZTogc2NhbGVUcmFuc2xhdGUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRyYW5zbGF0ZSBYXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdHJhbnNsYXRlXG4gICAgICAgKi9cbiAgICAgICd0cmFuc2xhdGUteCc6IFt7XG4gICAgICAgICd0cmFuc2xhdGUteCc6IHNjYWxlVHJhbnNsYXRlKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUcmFuc2xhdGUgWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RyYW5zbGF0ZVxuICAgICAgICovXG4gICAgICAndHJhbnNsYXRlLXknOiBbe1xuICAgICAgICAndHJhbnNsYXRlLXknOiBzY2FsZVRyYW5zbGF0ZSgpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVHJhbnNsYXRlIFpcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90cmFuc2xhdGVcbiAgICAgICAqL1xuICAgICAgJ3RyYW5zbGF0ZS16JzogW3tcbiAgICAgICAgJ3RyYW5zbGF0ZS16Jzogc2NhbGVUcmFuc2xhdGUoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRyYW5zbGF0ZSBOb25lXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdHJhbnNsYXRlXG4gICAgICAgKi9cbiAgICAgICd0cmFuc2xhdGUtbm9uZSc6IFsndHJhbnNsYXRlLW5vbmUnXSxcbiAgICAgIC8qKlxuICAgICAgICogWm9vbVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3pvb21cbiAgICAgICAqL1xuICAgICAgem9vbTogW3tcbiAgICAgICAgem9vbTogW2lzSW50ZWdlciwgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gICAgICAvLyAtLS0gSW50ZXJhY3Rpdml0eSAtLS1cbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBBY2NlbnQgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9hY2NlbnQtY29sb3JcbiAgICAgICAqL1xuICAgICAgYWNjZW50OiBbe1xuICAgICAgICBhY2NlbnQ6IHNjYWxlQ29sb3IoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIEFwcGVhcmFuY2VcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9hcHBlYXJhbmNlXG4gICAgICAgKi9cbiAgICAgIGFwcGVhcmFuY2U6IFt7XG4gICAgICAgIGFwcGVhcmFuY2U6IFsnbm9uZScsICdhdXRvJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBDYXJldCBDb2xvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2p1c3QtaW4tdGltZS1tb2RlI2NhcmV0LWNvbG9yLXV0aWxpdGllc1xuICAgICAgICovXG4gICAgICAnY2FyZXQtY29sb3InOiBbe1xuICAgICAgICBjYXJldDogc2NhbGVDb2xvcigpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQ29sb3IgU2NoZW1lXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY29sb3Itc2NoZW1lXG4gICAgICAgKi9cbiAgICAgICdjb2xvci1zY2hlbWUnOiBbe1xuICAgICAgICBzY2hlbWU6IFsnbm9ybWFsJywgJ2RhcmsnLCAnbGlnaHQnLCAnbGlnaHQtZGFyaycsICdvbmx5LWRhcmsnLCAnb25seS1saWdodCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogQ3Vyc29yXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvY3Vyc29yXG4gICAgICAgKi9cbiAgICAgIGN1cnNvcjogW3tcbiAgICAgICAgY3Vyc29yOiBbJ2F1dG8nLCAnZGVmYXVsdCcsICdwb2ludGVyJywgJ3dhaXQnLCAndGV4dCcsICdtb3ZlJywgJ2hlbHAnLCAnbm90LWFsbG93ZWQnLCAnbm9uZScsICdjb250ZXh0LW1lbnUnLCAncHJvZ3Jlc3MnLCAnY2VsbCcsICdjcm9zc2hhaXInLCAndmVydGljYWwtdGV4dCcsICdhbGlhcycsICdjb3B5JywgJ25vLWRyb3AnLCAnZ3JhYicsICdncmFiYmluZycsICdhbGwtc2Nyb2xsJywgJ2NvbC1yZXNpemUnLCAncm93LXJlc2l6ZScsICduLXJlc2l6ZScsICdlLXJlc2l6ZScsICdzLXJlc2l6ZScsICd3LXJlc2l6ZScsICduZS1yZXNpemUnLCAnbnctcmVzaXplJywgJ3NlLXJlc2l6ZScsICdzdy1yZXNpemUnLCAnZXctcmVzaXplJywgJ25zLXJlc2l6ZScsICduZXN3LXJlc2l6ZScsICdud3NlLXJlc2l6ZScsICd6b29tLWluJywgJ3pvb20tb3V0JywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBGaWVsZCBTaXppbmdcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9maWVsZC1zaXppbmdcbiAgICAgICAqL1xuICAgICAgJ2ZpZWxkLXNpemluZyc6IFt7XG4gICAgICAgICdmaWVsZC1zaXppbmcnOiBbJ2ZpeGVkJywgJ2NvbnRlbnQnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFBvaW50ZXIgRXZlbnRzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvcG9pbnRlci1ldmVudHNcbiAgICAgICAqL1xuICAgICAgJ3BvaW50ZXItZXZlbnRzJzogW3tcbiAgICAgICAgJ3BvaW50ZXItZXZlbnRzJzogWydhdXRvJywgJ25vbmUnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFJlc2l6ZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Jlc2l6ZVxuICAgICAgICovXG4gICAgICByZXNpemU6IFt7XG4gICAgICAgIHJlc2l6ZTogWydub25lJywgJycsICd5JywgJ3gnXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBCZWhhdmlvclxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1iZWhhdmlvclxuICAgICAgICovXG4gICAgICAnc2Nyb2xsLWJlaGF2aW9yJzogW3tcbiAgICAgICAgc2Nyb2xsOiBbJ2F1dG8nLCAnc21vb3RoJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGxiYXIgVGh1bWIgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGxiYXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbGJhci10aHVtYi1jb2xvcic6IFt7XG4gICAgICAgICdzY3JvbGxiYXItdGh1bWInOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGxiYXIgVHJhY2sgQ29sb3JcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGxiYXItY29sb3JcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbGJhci10cmFjay1jb2xvcic6IFt7XG4gICAgICAgICdzY3JvbGxiYXItdHJhY2snOiBzY2FsZUNvbG9yKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGxiYXIgR3V0dGVyXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsYmFyLWd1dHRlclxuICAgICAgICovXG4gICAgICAnc2Nyb2xsYmFyLWd1dHRlcic6IFt7XG4gICAgICAgICdzY3JvbGxiYXItZ3V0dGVyJzogWydhdXRvJywgJ3N0YWJsZScsICdib3RoJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGxiYXIgV2lkdGhcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGxiYXItd2lkdGhcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbGJhci13JzogW3tcbiAgICAgICAgc2Nyb2xsYmFyOiBbJ2F1dG8nLCAndGhpbicsICdub25lJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGwgTWFyZ2luXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLW1hcmdpblxuICAgICAgICovXG4gICAgICAnc2Nyb2xsLW0nOiBbe1xuICAgICAgICAnc2Nyb2xsLW0nOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIE1hcmdpbiBJbmxpbmVcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbXgnOiBbe1xuICAgICAgICAnc2Nyb2xsLW14Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBNYXJnaW4gQmxvY2tcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbXknOiBbe1xuICAgICAgICAnc2Nyb2xsLW15Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBNYXJnaW4gSW5saW5lIFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLW1hcmdpblxuICAgICAgICovXG4gICAgICAnc2Nyb2xsLW1zJzogW3tcbiAgICAgICAgJ3Njcm9sbC1tcyc6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGwgTWFyZ2luIElubGluZSBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbWUnOiBbe1xuICAgICAgICAnc2Nyb2xsLW1lJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBNYXJnaW4gQmxvY2sgU3RhcnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbWJzJzogW3tcbiAgICAgICAgJ3Njcm9sbC1tYnMnOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIE1hcmdpbiBCbG9jayBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbWJlJzogW3tcbiAgICAgICAgJ3Njcm9sbC1tYmUnOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIE1hcmdpbiBUb3BcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbXQnOiBbe1xuICAgICAgICAnc2Nyb2xsLW10Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBNYXJnaW4gUmlnaHRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbXInOiBbe1xuICAgICAgICAnc2Nyb2xsLW1yJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBNYXJnaW4gQm90dG9tXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLW1hcmdpblxuICAgICAgICovXG4gICAgICAnc2Nyb2xsLW1iJzogW3tcbiAgICAgICAgJ3Njcm9sbC1tYic6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGwgTWFyZ2luIExlZnRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtbWFyZ2luXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtbWwnOiBbe1xuICAgICAgICAnc2Nyb2xsLW1sJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1wJzogW3tcbiAgICAgICAgJ3Njcm9sbC1wJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nIElubGluZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1wYWRkaW5nXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtcHgnOiBbe1xuICAgICAgICAnc2Nyb2xsLXB4Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nIEJsb2NrXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1weSc6IFt7XG4gICAgICAgICdzY3JvbGwtcHknOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFBhZGRpbmcgSW5saW5lIFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1wcyc6IFt7XG4gICAgICAgICdzY3JvbGwtcHMnOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFBhZGRpbmcgSW5saW5lIEVuZFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1wYWRkaW5nXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtcGUnOiBbe1xuICAgICAgICAnc2Nyb2xsLXBlJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nIEJsb2NrIFN0YXJ0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1wYnMnOiBbe1xuICAgICAgICAnc2Nyb2xsLXBicyc6IHNjYWxlVW5hbWJpZ3VvdXNTcGFjaW5nKClcbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBTY3JvbGwgUGFkZGluZyBCbG9jayBFbmRcbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy9zY3JvbGwtcGFkZGluZ1xuICAgICAgICovXG4gICAgICAnc2Nyb2xsLXBiZSc6IFt7XG4gICAgICAgICdzY3JvbGwtcGJlJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nIFRvcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1wYWRkaW5nXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtcHQnOiBbe1xuICAgICAgICAnc2Nyb2xsLXB0Jzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBQYWRkaW5nIFJpZ2h0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1wcic6IFt7XG4gICAgICAgICdzY3JvbGwtcHInOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFBhZGRpbmcgQm90dG9tXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXBhZGRpbmdcbiAgICAgICAqL1xuICAgICAgJ3Njcm9sbC1wYic6IFt7XG4gICAgICAgICdzY3JvbGwtcGInOiBzY2FsZVVuYW1iaWd1b3VzU3BhY2luZygpXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFBhZGRpbmcgTGVmdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1wYWRkaW5nXG4gICAgICAgKi9cbiAgICAgICdzY3JvbGwtcGwnOiBbe1xuICAgICAgICAnc2Nyb2xsLXBsJzogc2NhbGVVbmFtYmlndW91c1NwYWNpbmcoKVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFNjcm9sbCBTbmFwIEFsaWduXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXNuYXAtYWxpZ25cbiAgICAgICAqL1xuICAgICAgJ3NuYXAtYWxpZ24nOiBbe1xuICAgICAgICBzbmFwOiBbJ3N0YXJ0JywgJ2VuZCcsICdjZW50ZXInLCAnYWxpZ24tbm9uZSddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFNuYXAgU3RvcFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1zbmFwLXN0b3BcbiAgICAgICAqL1xuICAgICAgJ3NuYXAtc3RvcCc6IFt7XG4gICAgICAgIHNuYXA6IFsnbm9ybWFsJywgJ2Fsd2F5cyddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFNuYXAgVHlwZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3Njcm9sbC1zbmFwLXR5cGVcbiAgICAgICAqL1xuICAgICAgJ3NuYXAtdHlwZSc6IFt7XG4gICAgICAgIHNuYXA6IFsnbm9uZScsICd4JywgJ3knLCAnYm90aCddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU2Nyb2xsIFNuYXAgVHlwZSBTdHJpY3RuZXNzXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc2Nyb2xsLXNuYXAtdHlwZVxuICAgICAgICovXG4gICAgICAnc25hcC1zdHJpY3RuZXNzJzogW3tcbiAgICAgICAgc25hcDogWydtYW5kYXRvcnknLCAncHJveGltaXR5J11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUb3VjaCBBY3Rpb25cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90b3VjaC1hY3Rpb25cbiAgICAgICAqL1xuICAgICAgdG91Y2g6IFt7XG4gICAgICAgIHRvdWNoOiBbJ2F1dG8nLCAnbm9uZScsICdtYW5pcHVsYXRpb24nXVxuICAgICAgfV0sXG4gICAgICAvKipcbiAgICAgICAqIFRvdWNoIEFjdGlvbiBYXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdG91Y2gtYWN0aW9uXG4gICAgICAgKi9cbiAgICAgICd0b3VjaC14JzogW3tcbiAgICAgICAgJ3RvdWNoLXBhbic6IFsneCcsICdsZWZ0JywgJ3JpZ2h0J11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBUb3VjaCBBY3Rpb24gWVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3RvdWNoLWFjdGlvblxuICAgICAgICovXG4gICAgICAndG91Y2gteSc6IFt7XG4gICAgICAgICd0b3VjaC1wYW4nOiBbJ3knLCAndXAnLCAnZG93biddXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogVG91Y2ggQWN0aW9uIFBpbmNoIFpvb21cbiAgICAgICAqIEBzZWUgaHR0cHM6Ly90YWlsd2luZGNzcy5jb20vZG9jcy90b3VjaC1hY3Rpb25cbiAgICAgICAqL1xuICAgICAgJ3RvdWNoLXB6JzogWyd0b3VjaC1waW5jaC16b29tJ10sXG4gICAgICAvKipcbiAgICAgICAqIFVzZXIgU2VsZWN0XG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvdXNlci1zZWxlY3RcbiAgICAgICAqL1xuICAgICAgc2VsZWN0OiBbe1xuICAgICAgICBzZWxlY3Q6IFsnbm9uZScsICd0ZXh0JywgJ2FsbCcsICdhdXRvJ11cbiAgICAgIH1dLFxuICAgICAgLyoqXG4gICAgICAgKiBXaWxsIENoYW5nZVxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL3dpbGwtY2hhbmdlXG4gICAgICAgKi9cbiAgICAgICd3aWxsLWNoYW5nZSc6IFt7XG4gICAgICAgICd3aWxsLWNoYW5nZSc6IFsnYXV0bycsICdzY3JvbGwnLCAnY29udGVudHMnLCAndHJhbnNmb3JtJywgaXNBcmJpdHJhcnlWYXJpYWJsZSwgaXNBcmJpdHJhcnlWYWx1ZV1cbiAgICAgIH1dLFxuICAgICAgLy8gLS0tLS0tLS0tLS1cbiAgICAgIC8vIC0tLSBTVkcgLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLVxuICAgICAgLyoqXG4gICAgICAgKiBGaWxsXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3MvZmlsbFxuICAgICAgICovXG4gICAgICBmaWxsOiBbe1xuICAgICAgICBmaWxsOiBbJ25vbmUnLCAuLi5zY2FsZUNvbG9yKCldXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU3Ryb2tlIFdpZHRoXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc3Ryb2tlLXdpZHRoXG4gICAgICAgKi9cbiAgICAgICdzdHJva2Utdyc6IFt7XG4gICAgICAgIHN0cm9rZTogW2lzTnVtYmVyLCBpc0FyYml0cmFyeVZhcmlhYmxlTGVuZ3RoLCBpc0FyYml0cmFyeUxlbmd0aCwgaXNBcmJpdHJhcnlOdW1iZXJdXG4gICAgICB9XSxcbiAgICAgIC8qKlxuICAgICAgICogU3Ryb2tlXG4gICAgICAgKiBAc2VlIGh0dHBzOi8vdGFpbHdpbmRjc3MuY29tL2RvY3Mvc3Ryb2tlXG4gICAgICAgKi9cbiAgICAgIHN0cm9rZTogW3tcbiAgICAgICAgc3Ryb2tlOiBbJ25vbmUnLCAuLi5zY2FsZUNvbG9yKCldXG4gICAgICB9XSxcbiAgICAgIC8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICAgICAgLy8gLS0tIEFjY2Vzc2liaWxpdHkgLS0tXG4gICAgICAvLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS1cbiAgICAgIC8qKlxuICAgICAgICogRm9yY2VkIENvbG9yIEFkanVzdFxuICAgICAgICogQHNlZSBodHRwczovL3RhaWx3aW5kY3NzLmNvbS9kb2NzL2ZvcmNlZC1jb2xvci1hZGp1c3RcbiAgICAgICAqL1xuICAgICAgJ2ZvcmNlZC1jb2xvci1hZGp1c3QnOiBbe1xuICAgICAgICAnZm9yY2VkLWNvbG9yLWFkanVzdCc6IFsnYXV0bycsICdub25lJ11cbiAgICAgIH1dXG4gICAgfSxcbiAgICBjb25mbGljdGluZ0NsYXNzR3JvdXBzOiB7XG4gICAgICAnY29udGFpbmVyLW5hbWVkJzogWydjb250YWluZXItdHlwZSddLFxuICAgICAgb3ZlcmZsb3c6IFsnb3ZlcmZsb3cteCcsICdvdmVyZmxvdy15J10sXG4gICAgICBvdmVyc2Nyb2xsOiBbJ292ZXJzY3JvbGwteCcsICdvdmVyc2Nyb2xsLXknXSxcbiAgICAgIGluc2V0OiBbJ2luc2V0LXgnLCAnaW5zZXQteScsICdpbnNldC1icycsICdpbnNldC1iZScsICdzdGFydCcsICdlbmQnLCAndG9wJywgJ3JpZ2h0JywgJ2JvdHRvbScsICdsZWZ0J10sXG4gICAgICAnaW5zZXQteCc6IFsncmlnaHQnLCAnbGVmdCddLFxuICAgICAgJ2luc2V0LXknOiBbJ3RvcCcsICdib3R0b20nXSxcbiAgICAgIGZsZXg6IFsnYmFzaXMnLCAnZ3JvdycsICdzaHJpbmsnXSxcbiAgICAgIGdhcDogWydnYXAteCcsICdnYXAteSddLFxuICAgICAgcDogWydweCcsICdweScsICdwcycsICdwZScsICdwYnMnLCAncGJlJywgJ3B0JywgJ3ByJywgJ3BiJywgJ3BsJ10sXG4gICAgICBweDogWydwcicsICdwbCddLFxuICAgICAgcHk6IFsncHQnLCAncGInXSxcbiAgICAgIG06IFsnbXgnLCAnbXknLCAnbXMnLCAnbWUnLCAnbWJzJywgJ21iZScsICdtdCcsICdtcicsICdtYicsICdtbCddLFxuICAgICAgbXg6IFsnbXInLCAnbWwnXSxcbiAgICAgIG15OiBbJ210JywgJ21iJ10sXG4gICAgICBzaXplOiBbJ3cnLCAnaCddLFxuICAgICAgJ2ZvbnQtc2l6ZSc6IFsnbGVhZGluZyddLFxuICAgICAgJ2Z2bi1ub3JtYWwnOiBbJ2Z2bi1vcmRpbmFsJywgJ2Z2bi1zbGFzaGVkLXplcm8nLCAnZnZuLWZpZ3VyZScsICdmdm4tc3BhY2luZycsICdmdm4tZnJhY3Rpb24nXSxcbiAgICAgICdmdm4tb3JkaW5hbCc6IFsnZnZuLW5vcm1hbCddLFxuICAgICAgJ2Z2bi1zbGFzaGVkLXplcm8nOiBbJ2Z2bi1ub3JtYWwnXSxcbiAgICAgICdmdm4tZmlndXJlJzogWydmdm4tbm9ybWFsJ10sXG4gICAgICAnZnZuLXNwYWNpbmcnOiBbJ2Z2bi1ub3JtYWwnXSxcbiAgICAgICdmdm4tZnJhY3Rpb24nOiBbJ2Z2bi1ub3JtYWwnXSxcbiAgICAgICdsaW5lLWNsYW1wJzogWydkaXNwbGF5JywgJ292ZXJmbG93J10sXG4gICAgICByb3VuZGVkOiBbJ3JvdW5kZWQtcycsICdyb3VuZGVkLWUnLCAncm91bmRlZC10JywgJ3JvdW5kZWQtcicsICdyb3VuZGVkLWInLCAncm91bmRlZC1sJywgJ3JvdW5kZWQtc3MnLCAncm91bmRlZC1zZScsICdyb3VuZGVkLWVlJywgJ3JvdW5kZWQtZXMnLCAncm91bmRlZC10bCcsICdyb3VuZGVkLXRyJywgJ3JvdW5kZWQtYnInLCAncm91bmRlZC1ibCddLFxuICAgICAgJ3JvdW5kZWQtcyc6IFsncm91bmRlZC1zcycsICdyb3VuZGVkLWVzJ10sXG4gICAgICAncm91bmRlZC1lJzogWydyb3VuZGVkLXNlJywgJ3JvdW5kZWQtZWUnXSxcbiAgICAgICdyb3VuZGVkLXQnOiBbJ3JvdW5kZWQtdGwnLCAncm91bmRlZC10ciddLFxuICAgICAgJ3JvdW5kZWQtcic6IFsncm91bmRlZC10cicsICdyb3VuZGVkLWJyJ10sXG4gICAgICAncm91bmRlZC1iJzogWydyb3VuZGVkLWJyJywgJ3JvdW5kZWQtYmwnXSxcbiAgICAgICdyb3VuZGVkLWwnOiBbJ3JvdW5kZWQtdGwnLCAncm91bmRlZC1ibCddLFxuICAgICAgJ2JvcmRlci1zcGFjaW5nJzogWydib3JkZXItc3BhY2luZy14JywgJ2JvcmRlci1zcGFjaW5nLXknXSxcbiAgICAgICdib3JkZXItdyc6IFsnYm9yZGVyLXcteCcsICdib3JkZXItdy15JywgJ2JvcmRlci13LXMnLCAnYm9yZGVyLXctZScsICdib3JkZXItdy1icycsICdib3JkZXItdy1iZScsICdib3JkZXItdy10JywgJ2JvcmRlci13LXInLCAnYm9yZGVyLXctYicsICdib3JkZXItdy1sJ10sXG4gICAgICAnYm9yZGVyLXcteCc6IFsnYm9yZGVyLXctcicsICdib3JkZXItdy1sJ10sXG4gICAgICAnYm9yZGVyLXcteSc6IFsnYm9yZGVyLXctdCcsICdib3JkZXItdy1iJ10sXG4gICAgICAnYm9yZGVyLWNvbG9yJzogWydib3JkZXItY29sb3IteCcsICdib3JkZXItY29sb3IteScsICdib3JkZXItY29sb3ItcycsICdib3JkZXItY29sb3ItZScsICdib3JkZXItY29sb3ItYnMnLCAnYm9yZGVyLWNvbG9yLWJlJywgJ2JvcmRlci1jb2xvci10JywgJ2JvcmRlci1jb2xvci1yJywgJ2JvcmRlci1jb2xvci1iJywgJ2JvcmRlci1jb2xvci1sJ10sXG4gICAgICAnYm9yZGVyLWNvbG9yLXgnOiBbJ2JvcmRlci1jb2xvci1yJywgJ2JvcmRlci1jb2xvci1sJ10sXG4gICAgICAnYm9yZGVyLWNvbG9yLXknOiBbJ2JvcmRlci1jb2xvci10JywgJ2JvcmRlci1jb2xvci1iJ10sXG4gICAgICB0cmFuc2xhdGU6IFsndHJhbnNsYXRlLXgnLCAndHJhbnNsYXRlLXknLCAndHJhbnNsYXRlLW5vbmUnXSxcbiAgICAgICd0cmFuc2xhdGUtbm9uZSc6IFsndHJhbnNsYXRlJywgJ3RyYW5zbGF0ZS14JywgJ3RyYW5zbGF0ZS15JywgJ3RyYW5zbGF0ZS16J10sXG4gICAgICAnc2Nyb2xsLW0nOiBbJ3Njcm9sbC1teCcsICdzY3JvbGwtbXknLCAnc2Nyb2xsLW1zJywgJ3Njcm9sbC1tZScsICdzY3JvbGwtbWJzJywgJ3Njcm9sbC1tYmUnLCAnc2Nyb2xsLW10JywgJ3Njcm9sbC1tcicsICdzY3JvbGwtbWInLCAnc2Nyb2xsLW1sJ10sXG4gICAgICAnc2Nyb2xsLW14JzogWydzY3JvbGwtbXInLCAnc2Nyb2xsLW1sJ10sXG4gICAgICAnc2Nyb2xsLW15JzogWydzY3JvbGwtbXQnLCAnc2Nyb2xsLW1iJ10sXG4gICAgICAnc2Nyb2xsLXAnOiBbJ3Njcm9sbC1weCcsICdzY3JvbGwtcHknLCAnc2Nyb2xsLXBzJywgJ3Njcm9sbC1wZScsICdzY3JvbGwtcGJzJywgJ3Njcm9sbC1wYmUnLCAnc2Nyb2xsLXB0JywgJ3Njcm9sbC1wcicsICdzY3JvbGwtcGInLCAnc2Nyb2xsLXBsJ10sXG4gICAgICAnc2Nyb2xsLXB4JzogWydzY3JvbGwtcHInLCAnc2Nyb2xsLXBsJ10sXG4gICAgICAnc2Nyb2xsLXB5JzogWydzY3JvbGwtcHQnLCAnc2Nyb2xsLXBiJ10sXG4gICAgICB0b3VjaDogWyd0b3VjaC14JywgJ3RvdWNoLXknLCAndG91Y2gtcHonXSxcbiAgICAgICd0b3VjaC14JzogWyd0b3VjaCddLFxuICAgICAgJ3RvdWNoLXknOiBbJ3RvdWNoJ10sXG4gICAgICAndG91Y2gtcHonOiBbJ3RvdWNoJ11cbiAgICB9LFxuICAgIGNvbmZsaWN0aW5nQ2xhc3NHcm91cE1vZGlmaWVyczoge1xuICAgICAgJ2ZvbnQtc2l6ZSc6IFsnbGVhZGluZyddXG4gICAgfSxcbiAgICBwb3N0Zml4TG9va3VwQ2xhc3NHcm91cHM6IFsnY29udGFpbmVyLXR5cGUnXSxcbiAgICBvcmRlclNlbnNpdGl2ZU1vZGlmaWVyczogWycqJywgJyoqJywgJ2FmdGVyJywgJ2JhY2tkcm9wJywgJ2JlZm9yZScsICdkZXRhaWxzLWNvbnRlbnQnLCAnZmlsZScsICdmaXJzdC1sZXR0ZXInLCAnZmlyc3QtbGluZScsICdtYXJrZXInLCAncGxhY2Vob2xkZXInLCAnc2VsZWN0aW9uJ11cbiAgfTtcbn07XG5cbi8qKlxuICogQHBhcmFtIGJhc2VDb25maWcgQ29uZmlnIHdoZXJlIG90aGVyIGNvbmZpZyB3aWxsIGJlIG1lcmdlZCBpbnRvLiBUaGlzIG9iamVjdCB3aWxsIGJlIG11dGF0ZWQuXG4gKiBAcGFyYW0gY29uZmlnRXh0ZW5zaW9uIFBhcnRpYWwgY29uZmlnIHRvIG1lcmdlIGludG8gdGhlIGBiYXNlQ29uZmlnYC5cbiAqL1xuY29uc3QgbWVyZ2VDb25maWdzID0gKGJhc2VDb25maWcsIHtcbiAgY2FjaGVTaXplLFxuICBwcmVmaXgsXG4gIGV4cGVyaW1lbnRhbFBhcnNlQ2xhc3NOYW1lLFxuICBleHRlbmQgPSB7fSxcbiAgb3ZlcnJpZGUgPSB7fVxufSkgPT4ge1xuICBvdmVycmlkZVByb3BlcnR5KGJhc2VDb25maWcsICdjYWNoZVNpemUnLCBjYWNoZVNpemUpO1xuICBvdmVycmlkZVByb3BlcnR5KGJhc2VDb25maWcsICdwcmVmaXgnLCBwcmVmaXgpO1xuICBvdmVycmlkZVByb3BlcnR5KGJhc2VDb25maWcsICdleHBlcmltZW50YWxQYXJzZUNsYXNzTmFtZScsIGV4cGVyaW1lbnRhbFBhcnNlQ2xhc3NOYW1lKTtcbiAgb3ZlcnJpZGVDb25maWdQcm9wZXJ0aWVzKGJhc2VDb25maWcudGhlbWUsIG92ZXJyaWRlLnRoZW1lKTtcbiAgb3ZlcnJpZGVDb25maWdQcm9wZXJ0aWVzKGJhc2VDb25maWcuY2xhc3NHcm91cHMsIG92ZXJyaWRlLmNsYXNzR3JvdXBzKTtcbiAgb3ZlcnJpZGVDb25maWdQcm9wZXJ0aWVzKGJhc2VDb25maWcuY29uZmxpY3RpbmdDbGFzc0dyb3Vwcywgb3ZlcnJpZGUuY29uZmxpY3RpbmdDbGFzc0dyb3Vwcyk7XG4gIG92ZXJyaWRlQ29uZmlnUHJvcGVydGllcyhiYXNlQ29uZmlnLmNvbmZsaWN0aW5nQ2xhc3NHcm91cE1vZGlmaWVycywgb3ZlcnJpZGUuY29uZmxpY3RpbmdDbGFzc0dyb3VwTW9kaWZpZXJzKTtcbiAgb3ZlcnJpZGVQcm9wZXJ0eShiYXNlQ29uZmlnLCAncG9zdGZpeExvb2t1cENsYXNzR3JvdXBzJywgb3ZlcnJpZGUucG9zdGZpeExvb2t1cENsYXNzR3JvdXBzKTtcbiAgb3ZlcnJpZGVQcm9wZXJ0eShiYXNlQ29uZmlnLCAnb3JkZXJTZW5zaXRpdmVNb2RpZmllcnMnLCBvdmVycmlkZS5vcmRlclNlbnNpdGl2ZU1vZGlmaWVycyk7XG4gIG1lcmdlQ29uZmlnUHJvcGVydGllcyhiYXNlQ29uZmlnLnRoZW1lLCBleHRlbmQudGhlbWUpO1xuICBtZXJnZUNvbmZpZ1Byb3BlcnRpZXMoYmFzZUNvbmZpZy5jbGFzc0dyb3VwcywgZXh0ZW5kLmNsYXNzR3JvdXBzKTtcbiAgbWVyZ2VDb25maWdQcm9wZXJ0aWVzKGJhc2VDb25maWcuY29uZmxpY3RpbmdDbGFzc0dyb3VwcywgZXh0ZW5kLmNvbmZsaWN0aW5nQ2xhc3NHcm91cHMpO1xuICBtZXJnZUNvbmZpZ1Byb3BlcnRpZXMoYmFzZUNvbmZpZy5jb25mbGljdGluZ0NsYXNzR3JvdXBNb2RpZmllcnMsIGV4dGVuZC5jb25mbGljdGluZ0NsYXNzR3JvdXBNb2RpZmllcnMpO1xuICBtZXJnZUFycmF5UHJvcGVydGllcyhiYXNlQ29uZmlnLCBleHRlbmQsICdwb3N0Zml4TG9va3VwQ2xhc3NHcm91cHMnKTtcbiAgbWVyZ2VBcnJheVByb3BlcnRpZXMoYmFzZUNvbmZpZywgZXh0ZW5kLCAnb3JkZXJTZW5zaXRpdmVNb2RpZmllcnMnKTtcbiAgcmV0dXJuIGJhc2VDb25maWc7XG59O1xuY29uc3Qgb3ZlcnJpZGVQcm9wZXJ0eSA9IChiYXNlT2JqZWN0LCBvdmVycmlkZUtleSwgb3ZlcnJpZGVWYWx1ZSkgPT4ge1xuICBpZiAob3ZlcnJpZGVWYWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgYmFzZU9iamVjdFtvdmVycmlkZUtleV0gPSBvdmVycmlkZVZhbHVlO1xuICB9XG59O1xuY29uc3Qgb3ZlcnJpZGVDb25maWdQcm9wZXJ0aWVzID0gKGJhc2VPYmplY3QsIG92ZXJyaWRlT2JqZWN0KSA9PiB7XG4gIGlmIChvdmVycmlkZU9iamVjdCkge1xuICAgIGZvciAoY29uc3Qga2V5IGluIG92ZXJyaWRlT2JqZWN0KSB7XG4gICAgICBvdmVycmlkZVByb3BlcnR5KGJhc2VPYmplY3QsIGtleSwgb3ZlcnJpZGVPYmplY3Rba2V5XSk7XG4gICAgfVxuICB9XG59O1xuY29uc3QgbWVyZ2VDb25maWdQcm9wZXJ0aWVzID0gKGJhc2VPYmplY3QsIG1lcmdlT2JqZWN0KSA9PiB7XG4gIGlmIChtZXJnZU9iamVjdCkge1xuICAgIGZvciAoY29uc3Qga2V5IGluIG1lcmdlT2JqZWN0KSB7XG4gICAgICBtZXJnZUFycmF5UHJvcGVydGllcyhiYXNlT2JqZWN0LCBtZXJnZU9iamVjdCwga2V5KTtcbiAgICB9XG4gIH1cbn07XG5jb25zdCBtZXJnZUFycmF5UHJvcGVydGllcyA9IChiYXNlT2JqZWN0LCBtZXJnZU9iamVjdCwga2V5KSA9PiB7XG4gIGNvbnN0IG1lcmdlVmFsdWUgPSBtZXJnZU9iamVjdFtrZXldO1xuICBpZiAobWVyZ2VWYWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgYmFzZU9iamVjdFtrZXldID0gYmFzZU9iamVjdFtrZXldID8gYmFzZU9iamVjdFtrZXldLmNvbmNhdChtZXJnZVZhbHVlKSA6IG1lcmdlVmFsdWU7XG4gIH1cbn07XG5jb25zdCBleHRlbmRUYWlsd2luZE1lcmdlID0gKGNvbmZpZ0V4dGVuc2lvbiwgLi4uY3JlYXRlQ29uZmlnKSA9PiB0eXBlb2YgY29uZmlnRXh0ZW5zaW9uID09PSAnZnVuY3Rpb24nID8gY3JlYXRlVGFpbHdpbmRNZXJnZShnZXREZWZhdWx0Q29uZmlnLCBjb25maWdFeHRlbnNpb24sIC4uLmNyZWF0ZUNvbmZpZykgOiBjcmVhdGVUYWlsd2luZE1lcmdlKCgpID0+IG1lcmdlQ29uZmlncyhnZXREZWZhdWx0Q29uZmlnKCksIGNvbmZpZ0V4dGVuc2lvbiksIC4uLmNyZWF0ZUNvbmZpZyk7XG5jb25zdCB0d01lcmdlID0gLyojX19QVVJFX18qL2NyZWF0ZVRhaWx3aW5kTWVyZ2UoZ2V0RGVmYXVsdENvbmZpZyk7XG5leHBvcnQgeyBjcmVhdGVUYWlsd2luZE1lcmdlLCBleHRlbmRUYWlsd2luZE1lcmdlLCBmcm9tVGhlbWUsIGdldERlZmF1bHRDb25maWcsIG1lcmdlQ29uZmlncywgdHdKb2luLCB0d01lcmdlLCB2YWxpZGF0b3JzIH07XG4vLyMgc291cmNlTWFwcGluZ1VSTD1idW5kbGUtbWpzLm1qcy5tYXBcbiJdLCJtYXBwaW5ncyI6Ijs7OztBQUdBLElBQU0sZ0JBQWdCLFFBQVEsV0FBVztDQUV2QyxNQUFNLGdCQUFnQixJQUFJLE1BQU0sT0FBTyxTQUFTLE9BQU8sTUFBTTtDQUM3RCxLQUFLLElBQUksSUFBSSxHQUFHLElBQUksT0FBTyxRQUFRLEtBQ2pDLGNBQWMsS0FBSyxPQUFPO0NBRTVCLEtBQUssSUFBSSxJQUFJLEdBQUcsSUFBSSxPQUFPLFFBQVEsS0FDakMsY0FBYyxPQUFPLFNBQVMsS0FBSyxPQUFPO0NBRTVDLE9BQU87QUFDVDtBQUdBLElBQU0sOEJBQThCLGNBQWMsZUFBZTtDQUMvRDtDQUNBO0FBQ0Y7QUFFQSxJQUFNLHlCQUF5QiwyQkFBVyxJQUFJLElBQUksR0FBRyxhQUFhLE1BQU0sa0JBQWtCO0NBQ3hGO0NBQ0E7Q0FDQTtBQUNGO0FBQ0EsSUFBTSx1QkFBdUI7QUFDN0IsSUFBTSxrQkFBa0IsQ0FBQztBQUV6QixJQUFNLDRCQUE0QjtBQUNsQyxJQUFNLHlCQUF3QixXQUFVO0NBQ3RDLE1BQU0sV0FBVyxlQUFlLE1BQU07Q0FDdEMsTUFBTSxFQUNKLHdCQUNBLG1DQUNFO0NBQ0osTUFBTSxtQkFBa0IsY0FBYTtFQUNuQyxJQUFJLFVBQVUsV0FBVyxHQUFHLEtBQUssVUFBVSxTQUFTLEdBQUcsR0FDckQsT0FBTywrQkFBK0IsU0FBUztFQUVqRCxNQUFNLGFBQWEsVUFBVSxNQUFNLG9CQUFvQjtFQUd2RCxPQUFPLGtCQUFrQixZQUROLFdBQVcsT0FBTyxNQUFNLFdBQVcsU0FBUyxJ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