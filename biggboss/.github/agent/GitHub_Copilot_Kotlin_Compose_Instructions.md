
# GitHub Copilot Instructions
## Kotlin • Jetpack Compose • Android • Multiplatform

---

## 1. Core Principles

- Follow **Clean Architecture + MVI**
- Kotlin-first, Compose-only UI
- Unidirectional Data Flow (UDF)
- Production-ready, scalable, testable code
- No shortcuts, no legacy patterns

Use **MUST / MUST NOT** rules strictly.

---

## 2. Architecture Rules (Mandatory)

### Layers
- UI (Compose)
- UiState / UiEvent
- ViewModel
- Domain (UseCases)
- Data (Repository)

### File Naming
```
<Feature>Screen.kt
<Feature>ViewModel.kt
<Feature>UiState.kt
<Feature>UiEvent.kt
<Feature>Repository.kt
```

---

## 3. Jetpack Compose Rules

### Composables
- MUST be stateless
- MUST receive UiState + Event callback
- MUST NOT contain business logic
- MUST use Material 3

```kotlin
@Composable
fun LoginScreen(
    state: LoginUiState,
    onEvent: (LoginUiEvent) -> Unit
)
```

### State Hoisting
- NEVER use mutableStateOf in screen-level composables
- State comes only from ViewModel

---

## 4. ViewModel Rules

- Holds StateFlow<UiState>
- Handles UiEvent
- No Compose imports
- No Android UI references

```kotlin
@HiltViewModel
class LoginViewModel @Inject constructor(
    private val repo: AuthRepository
) : ViewModel()
```

---

## 5. UiState & UiEvent

### UiState
- data class
- Immutable
- Default values

### UiEvent
- sealed interface
- Represents user actions only

---

## 6. XML → Compose Migration Instructions

### Conversion Rules
- Convert XML layouts to Composables
- Replace:
  - LinearLayout / ConstraintLayout → Column / Row / Box
  - TextView → Text
  - Button → Button / FilledTonalButton
- Remove findViewById usage
- Fragment becomes Screen-level Composable

### Migration Output
For Fragment `ProfileFragment` generate:
- ProfileScreen.kt
- ProfileViewModel.kt
- ProfileUiState.kt
- ProfileUiEvent.kt

---

## 7. Compose Multiplatform Rules

- UI logic in commonMain
- Platform-specific code in androidMain / iosMain
- Avoid Android-only APIs in commonMain
- Use expect/actual for platform differences

```kotlin
expect fun platformName(): String
```

---

## 8. Navigation Rules

- Use Navigation Compose
- ViewModel MUST NOT navigate
- Emit navigation as SideEffect

---

## 9. Dependency Injection

- Use Hilt (Android)
- Constructor injection only
- No service locators

---

## 10. Error Handling

- Errors represented in UiState
- UI reacts to state only
- No try/catch in Composables

---

## 11. Testing Rules

### ViewModel
- JUnit + Turbine
- Test UiState transitions

### Compose UI
- composeTestRule
- Test behavior, not implementation

---

## 12. Performance Rules

- Prefer LazyColumn over Column + scroll
- Use remember only for UI optimization
- Use stable data classes

---

## 13. Anti-Patterns (Copilot MUST AVOID)

- mutableStateOf in ViewModel
- LiveData (use StateFlow)
- Business logic in Composables
- Navigation inside ViewModel
- Context usage in ViewModel
- XML layouts in new features
- God ViewModels
- Side-effects in Composables

---

## 14. Final Copilot Prompt (Paste This)

```
You are a senior Android Jetpack Compose engineer.

Follow Clean Architecture with MVI.
Use Kotlin + Jetpack Compose only.
UI must be stateless.
ViewModels expose StateFlow<UiState>.
Handle user actions via sealed UiEvent.
Use Hilt for dependency injection.
Use Material 3.
Avoid all listed anti-patterns.
Write clean, production-ready code.
```


---

# 15. Kotlin Coding Standards & Conventions (Industry Grade)

## 15.1 General Kotlin Standards

### Rule
Code must follow Kotlin official style guide and Android best practices.

- Prefer `val` over `var`
- Use meaningful names
- Keep functions small and focused

```kotlin
val userName: String
val isLoading: Boolean
```

---

## 15.2 Variable Naming

### Rule
Variable names must express intent.

- camelCase for variables/functions
- PascalCase for classes
- Boolean names start with is/has/can

```kotlin
val isUserLoggedIn: Boolean
val hasNetworkConnection: Boolean
```

---

## 15.3 Constants

### Rule
Avoid magic values.

```kotlin
private const val MAX_LOGIN_ATTEMPTS = 3
```

---

## 15.4 Function Design

### Rule
Functions must do one thing.

```kotlin
fun isEmailValid(email: String): Boolean =
    email.contains("@")
```

---

## 15.5 Null Safety

### Rule
Nullability must be explicit.

```kotlin
fun getUserName(user: User?): String =
    user?.name ?: "Guest"
```

---

## 15.6 UI State Variables

### Rule
All UI variables belong to UiState.

```kotlin
data class LoginUiState(
    val email: String = "",
    val isLoading: Boolean = false
)
```

---

## 15.7 User Input Handling

### Rule
User input must flow via UiEvent.

```kotlin
TextField(
    value = state.email,
    onValueChange = {
        onEvent(LoginUiEvent.EmailChanged(it))
    }
)
```

---

## 15.8 When Copilot Must Ask for Clarification

### Rule
Copilot must request clarification when requirements affect behavior.

- Validation rules unknown
- Navigation unclear
- API contracts missing

---

## 15.9 Formatting Rules

### Rule
Code must be readable and consistent.

```kotlin
fun LoginScreen(
    state: LoginUiState,
    onEvent: (LoginUiEvent) -> Unit,
)
```

---

## 15.10 Forbidden Practices

Copilot MUST NOT generate:
- `!!`
- `mutableStateOf` in ViewModel
- Logic in Composables
- Magic numbers

---

# Final Coding Instruction (Additive)

```text
Follow Kotlin official style guide.
Prefer val over var.
Avoid nullability unless required.
Never use !!.
Route all user input via UiEvent.
UiState must be immutable.
Ask for clarification when requirements are unclear.
```

