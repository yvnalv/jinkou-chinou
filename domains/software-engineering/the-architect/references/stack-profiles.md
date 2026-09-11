# Stack Profiles

Stack-specific detail for The Architect. `SKILL.md` defines the general process; this file tells you what to inventory, what to ask about, and how to verify for each kind of system.

How to use:

1. Detect every stack in the repository (`scripts/scan_repo.py` lists manifests and sub-projects).
2. Load the matching profile(s). Most real systems combine several, for example Web Backend + Web Frontend + Infrastructure.
3. If nothing matches, derive inventory categories from the stack's own conventions and say so.
4. Commands below are typical examples. Always prefer the commands the repository already uses (package.json scripts, Makefile, CI pipeline, README).

Contents:

1. Web Backend / API / Services
2. Web Frontend
3. Mobile
4. Desktop
5. Data, Analytics & ML
6. Infrastructure-as-Code & DevOps
7. Library, SDK & CLI
8. Systems, Embedded & C/C++
9. Game Development

---

## 1. Web Backend / API / Services

**Detect:** `*.csproj` / `*.sln` (ASP.NET), `pom.xml` / `build.gradle` (Spring), `package.json` with express / nest / fastify, `pyproject.toml` / `requirements.txt` with django / fastapi / flask, `go.mod`, `composer.json` (Laravel / Symfony), `Gemfile` (Rails), `Cargo.toml` with axum / actix, `serverless.yml`, `host.json` (Azure Functions).

**Inventory:**

- Controllers / endpoints / route handlers / minimal APIs / serverless functions
- Services / use cases / application handlers
- Repositories / DAOs / ORM models / entities / domain models
- DTOs / request and response schemas / commands / queries
- Validators
- Middleware / filters / interceptors
- Authentication / authorization
- Background jobs / workers / schedulers / queue and event consumers
- External integrations / API clients
- Database access, migrations, seed data
- Mappings and shared utilities
- Configuration key names (never values)

**Discovery concerns:** API versioning and who consumes the API, transactions and concurrency, idempotency of retries and webhooks, pagination, rate limits, multi-tenancy, audit logging.

**Verify:**

| Ecosystem | Typical commands |
|---|---|
| .NET | `dotnet restore`, `dotnet build`, `dotnet test` |
| Java / Kotlin | `mvn verify` or `./gradlew build test` |
| Node.js | `npm ci`, `npm run build`, `npm test`, `npx tsc --noEmit` for TypeScript |
| Python | `pip install -r requirements.txt` / `uv sync` / `poetry install`, `pytest`, `ruff check`, `mypy` if used |
| Go | `go build ./...`, `go vet ./...`, `go test ./...` |
| PHP | `composer install`, `vendor/bin/phpunit` or `php artisan test` |
| Ruby | `bundle install`, `bundle exec rspec` or `bin/rails test` |
| Rust | `cargo build`, `cargo test`, `cargo clippy` |

**No tests yet? Lightest conventional setup:** xUnit (.NET), JUnit 5 (Java / Kotlin), Vitest or Jest (Node.js), pytest (Python), `go test` (Go), PHPUnit or Pest (PHP), RSpec or Minitest (Ruby), built-in `cargo test` (Rust).

**.gitignore:** `bin/`, `obj/`, `target/`, `build/`, `dist/`, `node_modules/`, `.venv/`, `__pycache__/`, `vendor/` (only where the ecosystem does not commit vendored dependencies), `.env`, `appsettings.*.local.json`, `*.user`.

---

## 2. Web Frontend

**Detect:** `package.json` with react / vue / angular / svelte / next / nuxt, `angular.json`, `vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.js`, Razor / Blazor (`*.cshtml`, `*.razor`).

**Inventory:**

- Pages / views / screens / routes / layouts
- Components (shared vs feature-specific)
- Feature modules
- State management / stores
- API clients / HTTP abstractions / generated clients
- Models / types
- Hooks / composables / services
- Forms and validation
- Shared utilities, themes, design system
- Internationalization
- Build scripts, environment configuration, deployment scripts

**Discovery concerns:** SSR vs SPA vs static site, SEO, accessibility level, browser support, responsive layout, auth token handling, loading and error states, internationalization.

**Verify:** `npm ci`, `npm run build`, `npm run lint`, `npx tsc --noEmit`, `npm test`; end-to-end tests with Playwright or Cypress if present. Angular: `ng build`, `ng test`.

**No tests yet?** Vitest + Testing Library (Vite-based projects), Jest + Testing Library (others), Playwright for a few critical end-to-end flows.

**.gitignore:** `node_modules/`, `dist/`, `build/`, `.next/`, `.nuxt/`, `.svelte-kit/`, `.angular/`, `coverage/`, `.env*.local`.

---

## 3. Mobile

**Detect:** `*.xcodeproj` / `*.xcworkspace`, `Package.swift`, `Podfile` (iOS); `AndroidManifest.xml`, `build.gradle(.kts)` with the Android plugin (Android); `pubspec.yaml` (Flutter); `package.json` with react-native or expo, `app.json`, `metro.config.js` (React Native).

**Inventory:**

- Screens / views / navigation graph and deep links
- View models / state management (SwiftUI state, Jetpack ViewModel, Bloc / Riverpod / Provider, Redux / Zustand)
- API clients, offline cache, local database (Core Data, Room, SQLite, Hive)
- Background tasks and push notifications
- Platform permissions and entitlements (camera, location, notifications, …)
- Native modules / platform channels (Flutter, React Native)
- Build variants / flavors / schemes and environments
- Signing and store configuration (key names only)
- Analytics and crash reporting

**Discovery concerns:**

- Offline behavior and sync conflicts.
- Minimum OS versions and device classes.
- **Old app versions stay installed.** Backend and API changes must remain compatible with released app versions, or a forced-update mechanism must exist.
- App store review rules, privacy manifests and data-safety declarations.
- Permission prompts and what happens when the user denies them.

**Verify:**

| Platform | Typical commands |
|---|---|
| iOS | `xcodebuild -scheme <scheme> -destination 'platform=iOS Simulator,name=<device>' test` |
| Android | `./gradlew assembleDebug`, `./gradlew testDebugUnitTest`, `./gradlew lint` |
| Flutter | `flutter pub get`, `flutter analyze`, `flutter test` |
| React Native | `npm test`, `npx tsc --noEmit`, then a platform build as above |

A simulator, emulator, or device is often unavailable. Say so explicitly instead of claiming the check passed.

**No tests yet?** XCTest (iOS), JUnit + Robolectric (Android unit tests), `flutter_test` (Flutter), Jest + React Native Testing Library (React Native).

**.gitignore:** `Pods/` (unless the team commits it), `DerivedData/`, `xcuserdata/`, `*.xcuserstate`, `.gradle/`, `build/`, `local.properties`, `.dart_tool/`, `.flutter-plugins*`, `.expo/`, signing material (`*.jks`, `*.keystore`, `*.p12`, `*.mobileprovision`).

---

## 4. Desktop

**Detect:** WPF / WinForms / .NET MAUI (`*.csproj` with `UseWPF`, `UseWindowsForms`, or `UseMaui`), Electron (`electron` in `package.json`), Tauri (`src-tauri/`, `tauri.conf.json`), Qt (`*.pro`, CMake with Qt), JavaFX.

**Inventory:** windows / views / view models (MVVM), commands, IPC between main and renderer or backend processes, local storage and file access, OS integration (tray, notifications, file associations), auto-update, installer and packaging, native dependencies.

**Discovery concerns:** supported OS versions, offline behavior, installer and update channel, code signing, file-system permissions, high-DPI and multi-monitor behavior.

**Verify:** `dotnet build` / `dotnet test` (.NET), `npm run build` + `npm test` (Electron), `cargo test` + `cargo tauri build` (Tauri), CMake + `ctest` (Qt). UI automation is often unavailable; list the manual checks instead.

**No tests yet?** The language's standard unit test framework for view models and logic; keep UI tests for a few critical flows.

**.gitignore:** as for the underlying language, plus installer output (`out/`, `release/`, `*.msi`, `*.dmg`, `*.AppImage`).

---

## 5. Data, Analytics & ML

**Detect:** `*.ipynb`, `dbt_project.yml`, Airflow `dags/`, Prefect / Dagster projects, `environment.yml` (conda), `MLproject`, dependencies such as pandas, polars, pyspark, scikit-learn, torch, tensorflow.

**Inventory:**

- Data sources and sinks (databases, files, APIs, streams)
- Datasets, schemas, and data contracts
- Pipelines / DAGs / jobs and their schedules
- Transformations (SQL models, dataframe code)
- Features, models, training and evaluation code
- Experiment tracking and model registry
- Notebooks (exploratory vs production)
- Downstream consumers (dashboards, services, reports)

**Discovery concerns:**

- **Actors are often data consumers**, not app users: who reads the output and what decision it drives.
- Data volume, freshness / latency, and backfill needs.
- Data quality rules are business rules (null handling, deduplication, late-arriving data).
- Reproducibility: pinned dependencies, random seeds, dataset versions.
- PII, privacy, and retention.
- For ML: evaluation metrics and thresholds become **acceptance criteria**. Agree on the baseline to beat, and on bias and drift monitoring.

**Verify:** `pytest` on transformation logic with small fixture data, `dbt build` / `dbt test`, data-quality checks (dbt tests, Great Expectations, pandera), executing notebooks headlessly (`jupyter nbconvert --execute` or papermill), a dry run on a sample dataset. Never run against production data without explicit approval.

**No tests yet?** pytest with tiny fixture datasets; dbt schema tests (`unique`, `not_null`, `relationships`).

**.gitignore:** raw and generated data (`data/raw/`, large `*.csv` / `*.parquet` outputs; keep small test fixtures), `.ipynb_checkpoints/`, `mlruns/`, model artifacts (`*.pt`, `*.pkl`, `*.onnx`) unless tracked with Git LFS or DVC, `.env`.

---

## 6. Infrastructure-as-Code & DevOps

**Detect:** `*.tf` (Terraform / OpenTofu), `Pulumi.yaml`, `*.bicep`, CloudFormation / SAM templates, `Chart.yaml` (Helm), `kustomization.yaml`, Kubernetes manifests, Ansible playbooks, `Dockerfile`, CI files (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`).

**Inventory:** environments (dev / staging / prod) and how they differ, modules / stacks, resources, state backends, networking, IAM roles and service accounts, secrets management (secret names and store only), CI/CD pipelines and deployment flow, container images.

**Discovery concerns:** blast radius and which environments are shared, drift between code and reality, downtime tolerance, cost, compliance, who is allowed to apply changes.

**Verify:**

- Terraform: `terraform fmt -check`, `terraform init -backend=false`, `terraform validate`, `terraform plan` (review every destroy / replace), optionally `tflint` or `checkov`.
- Helm / Kubernetes: `helm lint`, `helm template`, schema validation with `kubeconform` or `kubectl apply --dry-run=client`.
- Docker: `docker build`.
- CI: validate pipeline syntax where a linter exists.

**Hard rules:** never run `apply`, `destroy`, `deploy`, or an equivalent against a shared or production environment without explicit approval. Report any planned destroy or replace as a risk.

**No tests yet?** `terraform validate` + `tflint` as the minimum; `terraform test` or Terratest for reusable modules.

**.gitignore:** `.terraform/`, `*.tfstate`, `*.tfstate.*`, `*.tfvars` files that hold secrets (commit a `*.tfvars.example`), `crash.log`, kubeconfig files, `.env`.

---

## 7. Library, SDK & CLI

**Detect:** package metadata meant for publishing (`pyproject.toml` with a build backend, `package.json` with `main` / `exports` and no app entry point, `PackageId` in a `*.csproj`, `[lib]` in `Cargo.toml`), CLI entry points (`bin` in `package.json`, `console_scripts`, cobra, click, System.CommandLine).

**Inventory:**

- Public API surface: exported modules, classes, functions, types; CLI commands, flags, exit codes, output formats
- Configuration options and defaults
- Extension points / plugins / hooks
- Supported runtime and platform versions
- Packaging and publishing pipeline
- Documentation and examples

**Discovery concerns:**

- **Actors are consumers**: developers and programs calling the API, or scripts calling the CLI.
- Backward compatibility and semantic versioning: which changes are breaking, and the deprecation policy.
- Output stability for CLIs whose output other scripts parse.
- Dependency footprint and licenses.

**Verify:** unit tests, building the package, running the examples, and a public-API compatibility check where tooling exists (for example `api-extractor`, `cargo-semver-checks`, `japicmp`, `Microsoft.CodeAnalysis.PublicApiAnalyzers`). For CLIs, snapshot-test `--help` and command output.

**No tests yet?** The ecosystem's standard unit test framework (see the Web Backend table) plus a smoke test that installs the built package in a clean environment.

**.gitignore:** as for the language, plus `*.egg-info/`, `dist/`, `*.nupkg`, `*.tgz`.

---

## 8. Systems, Embedded & C/C++

**Detect:** `CMakeLists.txt`, `Makefile`, `meson.build`, `*.vcxproj`, `conanfile.*`, `vcpkg.json`, `platformio.ini`, `*.ino`, linker scripts, RTOS configuration.

**Inventory:** build targets and configurations, modules and libraries, hardware abstraction layer and drivers, tasks / threads / interrupts, memory map and allocation strategy, communication protocols, toolchains and target boards, third-party dependencies.

**Discovery concerns:** memory and timing budgets, real-time constraints, target hardware and toolchain versions, safety or certification requirements, power use, update / flashing mechanism, undefined-behavior and memory-safety risks.

**Verify:** `cmake -S . -B build && cmake --build build && ctest --test-dir build`, `make test`, static analysis (`clang-tidy`, `cppcheck`), sanitizers (ASan / UBSan) on host builds. Hardware-in-the-loop testing is often unavailable; say so and list what must be checked on real hardware.

**No tests yet?** GoogleTest or Catch2 (C++), Unity or CMocka (C), host-side unit tests for hardware-independent logic.

**.gitignore:** `build/`, `cmake-build-*/`, `.pio/`, object files and binaries (`*.o`, `*.obj`, `*.a`, `*.lib`, `*.so`, `*.dll`, `*.exe`, `*.elf`, `*.hex`).

---

## 9. Game Development

**Detect:** Unity (`ProjectSettings/ProjectVersion.txt`, `Assets/`), Unreal (`*.uproject`), Godot (`project.godot`).

**Inventory:** scenes / levels, prefabs / blueprints / nodes, game systems (input, physics, AI, UI, audio), save data and persistence, asset pipeline, networking / multiplayer, platform build targets.

**Discovery concerns:** target platforms and performance budgets (frame rate, memory), save-data compatibility between versions, multiplayer authority model, large binary assets and merge conflicts.

**Verify:** engine test runners (Unity Test Framework in batch mode, Unreal Automation, GUT for Godot) and a platform build. Visual and gameplay checks usually need a human; list them.

**No tests yet?** Unity Test Framework (edit-mode tests for logic first), Unreal Automation Spec, GUT (Godot).

**.gitignore:** Unity `Library/`, `Temp/`, `Obj/`, `Logs/`, `UserSettings/`; Unreal `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`; Godot `.godot/`. Use Git LFS for large binary assets.
