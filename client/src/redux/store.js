import { createStore, combineReducers, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import thunk from 'redux-thunk'
import { cartReducer } from './reducers/cartReducer'
import { getProductDetailsReducer, getProductReducer } from './reducers/productReducer'
const reducer = combineReducers(
    {
        getProducts: getProductReducer,
        getProductDetails: getProductDetailsReducer,
        cart: cartReducer
    }
)
const middleware = [thunk];
const store = createStore(
    reducer,
    composeWithDevTools(applyMiddleware(...middleware))
)
export default store