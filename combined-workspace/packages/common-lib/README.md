# Common Library

The `common-lib` package is a shared library designed to provide common functionality and utilities that can be utilized by both Service A and Service B. 

## Purpose

The primary purpose of the `common-lib` is to encapsulate shared code, making it easier to maintain and reuse across different services within the workspace.

## Installation

To install the `common-lib`, you can use the following command:

```bash
npm install common-lib
```

or if you are using pnpm:

```bash
pnpm add common-lib
```

## Usage

To use the functionalities provided by the `common-lib`, you can import it in your service files as follows:

```typescript
import { someFunction } from 'common-lib';
```

## Development

To contribute to the `common-lib`, clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd common-lib
npm install
```

You can run tests and build the library using the following commands:

```bash
npm test
npm run build
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.