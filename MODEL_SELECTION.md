# 🤖 Gemini Model Selection Guide

## Available Models for FinAI

### 🚀 **Gemini 2.5 Models (Latest)**

#### **Gemini 2.5 Flash** - `"gemini-2.5-flash-exp"`
- ✅ **Fastest** response times
- ✅ **Most cost-effective**
- ✅ **Perfect for financial calculations and basic advice**
- ✅ **Recommended for most use cases**
- ✅ **Latest improvements** and optimizations
- ⚠️ Limited reasoning capabilities

#### **Gemini 2.5 Pro** - `"gemini-2.5-pro-exp"`
- ✅ **Most capable** and intelligent
- ✅ **Better reasoning** and complex analysis
- ✅ **Excellent for detailed financial planning**
- ✅ **Latest AI advancements**
- ⚠️ **Slower** response times
- ⚠️ **More expensive**

### 🔄 **Gemini 2.0 Models (Fallback)**

#### **Gemini 2.0 Flash** - `"gemini-2.0-flash-exp"`
- ✅ **Stable** and reliable
- ✅ **Good performance**
- ✅ **Fallback option** if 2.5 not available

#### **Gemini 2.0 Pro** - `"gemini-2.0-pro-exp"`
- ✅ **Capable** and intelligent
- ✅ **Good reasoning** capabilities
- ✅ **Alternative** to 2.5 Pro

## 🛠️ How to Change Models

### **Option 1: Edit agent_config.py**
```python
API_CONFIG = {
    "model": "gemini-2.5-flash-exp",  # Change this line
    # ... other settings
}
```

### **Option 2: Environment Variable (Advanced)**
```bash
export GEMINI_MODEL="gemini-2.5-pro-exp"
```

Then update `financial_advisor_chat.py`:
```python
model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL", API_CONFIG["model"]))
```

## 🎯 **Recommendations**

### **For Development/Testing:**
- Use `"gemini-2.5-flash-exp"` (fast, cheap)

### **For Production/Complex Queries:**
- Use `"gemini-2.5-pro-exp"` (better reasoning)

### **For Fallback:**
- Use `"gemini-2.0-flash-exp"` (stable, reliable)

## ⚠️ **Important Notes**

1. **Access Required**: Make sure you have access to Gemini 2.5 models
2. **API Limits**: Check your Google AI API quotas
3. **Cost**: Pro models are more expensive than Flash models
4. **Testing**: Always test with your specific use case

## 🔧 **Current Setting**
Your FinAI is currently configured to use: **`gemini-1.5-flash`** 